from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma

DB_FOLDER = "vectordb"

print("Loading models...")

llm = OllamaLLM(model="llama3:8b")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

db = Chroma(
    persist_directory=DB_FOLDER,
    embedding_function=embeddings
)

retriever = db.as_retriever(search_kwargs={"k": 8})

print("\n✅ OrgAgent CLI ready (type 'exit' to quit)\n")


def ask_question(question: str):
    docs = retriever.invoke(question)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are a strict question-answering system.

Rules:
1. Use ONLY the provided context.
2. Do NOT use prior knowledge.
3. If answer is not explicitly present, say: "Not found in documents".
4. Do NOT guess.

Context:
{context}

Question:
{question}

Answer:
"""

    return llm.invoke(prompt)



while True:
    q = input("Ask: ")

    if q.lower() == "exit":
        break

    answer = ask_question(q)

    print("\nAnswer:\n", answer, "\n")

docs = retriever.invoke(question)

print("\nRetrieved sources:")
for d in docs:
    print("-", d.metadata.get("source"))

