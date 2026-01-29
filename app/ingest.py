import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


PDF_FOLDER = "uploads"
DB_FOLDER = "vectordb"


def ingest():
    all_docs = []

    print("Scanning PDFs...")

    for file in os.listdir(PDF_FOLDER):
        if file.endswith(".pdf"):
            path = os.path.join(PDF_FOLDER, file)

            loader = PyPDFLoader(path)
            docs = loader.load()

            # attach metadata
            for d in docs:
                d.metadata["source"] = file

            all_docs.extend(docs)

            print(f"Loaded: {file}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300
    )


    chunks = splitter.split_documents(all_docs)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    print("Creating vector DB...")

    Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=DB_FOLDER
    )

    print("Done.")
    

if __name__ == "__main__":
    ingest()
