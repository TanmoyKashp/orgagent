import os
import sys
from typing import List, Tuple
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
INDEX_NAME = "orgagent"
PDF_FOLDER = "uploads"

# --- CORE FUNCTIONS ---

def get_llm():
    try:
        return ChatOpenAI(
            model="tngtech/deepseek-r1t2-chimera:free",
            openai_api_key=OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
        )
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        sys.exit(1)

def initialize_pinecone():
    try:
        pc = Pinecone(api_key = PINECONE_API_KEY)
        embeddings = OpenAIEmbeddings(
            model="openai/text-embedding-3-large",
            api_key=os.getenv("OPENROUTER_API_KEY"), 
            openai_api_base="https://openrouter.ai/api/v1"
            )

        if INDEX_NAME not in pc.list_indexes().names():
            print(f"Creating new Pinecone index: {INDEX_NAME}...")
            pc.create_index(
                name=INDEX_NAME,
                dimension=3072,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        return PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    except Exception as e:
        print(f"Pinecone Initialization Error: {e}")
        sys.exit(1)

def ingest_documents(vectorstore: PineconeVectorStore):
    if not os.path.exists(PDF_FOLDER):
        print(f"Warning: Folder '{PDF_FOLDER}' not found.")
        return

    all_docs = []
    try:
        files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
        if not files:
            print("No PDF files found to ingest.")
            return

        for file in files:
            path = os.path.join(PDF_FOLDER, file)
            loader = PyPDFLoader(path)
            docs = loader.load()
            for d in docs:
                d.metadata["source"] = file
            all_docs.extend(docs)
            print(f"Loaded: {file}")

        splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        chunks = splitter.split_documents(all_docs)

        print(f"Uploading {len(chunks)} chunks to Pinecone...")
        vectorstore.add_documents(chunks)
        print("Ingestion complete.")
    except Exception as e:
        print(f"Error during ingestion: {e}")

def get_answer(question: str, vectorstore: PineconeVectorStore, llm: ChatOpenAI) -> Tuple[str, List]:
    try:
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(question)
        
        context = "\n\n".join([d.page_content for d in docs])
        prompt = f"""You are a knowledgeable assistant with access to a document database. 
                Your task is to answer questions accurately based solely on the provided context.

                INSTRUCTIONS:
                - Use ONLY the information from the context below
                - If the context doesn't contain the answer, say "I couldn't find this information in the available documents"
                - Be concise but thorough
                - If information is partial, acknowledge what you found and what's missing
                - Cite the source document when possible

                CONTEXT:
                {context}

                USER QUESTION: {question}

                ANSWER:"""

        response = llm.invoke(prompt)
        return response.content, docs
    except Exception as e:
        return f"Error generating answer: {str(e)}", []


def main():
    vectorstore = initialize_pinecone()
    llm = get_llm()

    ingest_documents(vectorstore)

    while True:
        try:
            q = input("Ask: ").strip()
            if not q: continue
            if q.lower() == "exit": break

            answer, sources = get_answer(q, vectorstore, llm)
            
            print(f"\nAnswer:\n{answer}")
            if sources:
                source_names = {d.metadata.get("source", "Unknown") for d in sources}
                print(f"Sources: {', '.join(source_names)}")
            print("-" * 40)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()