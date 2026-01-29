import os
import shutil
import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma


# ======================================================
# CONFIG
# ======================================================

UPLOAD_FOLDER = "uploads"
DB_FOLDER = "vectordb"

EMBED_MODEL = "nomic-embed-text"   # fast embeddings
LLM_MODEL = "llama3:8b"            # answering model

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ======================================================
# LOAD MODELS (cached → faster UI)
# ======================================================

@st.cache_resource
def load_models():
    llm = OllamaLLM(model=LLM_MODEL)
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    return llm, embeddings


@st.cache_resource
def load_vectordb(embeddings):
    if not os.path.exists(DB_FOLDER):
        return None

    return Chroma(
        persist_directory=DB_FOLDER,
        embedding_function=embeddings
    )


# ======================================================
# INGESTION (build vector DB)
# ======================================================

def ingest_pdfs():
    # clear streamlit cache FIRST (releases DB lock)
    st.cache_resource.clear()

    if os.path.exists(DB_FOLDER):
        shutil.rmtree(DB_FOLDER)

    documents = []

    for file in os.listdir(UPLOAD_FOLDER):
        if file.endswith(".pdf"):
            path = os.path.join(UPLOAD_FOLDER, file)

            loader = PyPDFLoader(path)
            docs = loader.load()

            for d in docs:
                d.metadata["source"] = file

            documents.extend(docs)

    if not documents:
        return False

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300
    )

    chunks = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model=EMBED_MODEL)

    Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=DB_FOLDER
    )

    return True

# ======================================================
# QA LOGIC (simple + robust)
# ======================================================

def ask_question(question, retriever, llm):
    docs = retriever.invoke(question)

    if not docs:
        return "No relevant information found.", []

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are a strict document question-answering system.

Rules:
- Use ONLY the provided context
- Do NOT use outside knowledge
- If not present → say "Not found in documents"
- Do NOT guess

Context:
{context}

Question:
{question}

Answer:
"""

    answer = llm.invoke(prompt)

    sources = list(set(d.metadata.get("source", "unknown") for d in docs))

    return answer, sources


# ======================================================
# STREAMLIT UI
# ======================================================

st.set_page_config(page_title="OrgAgent", layout="wide")

st.title("🧠 OrgAgent — Local Document Assistant")


llm, embeddings = load_models()


# -----------------------
# Sidebar
# -----------------------

st.sidebar.header("📂 Documents")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        with open(os.path.join(UPLOAD_FOLDER, file.name), "wb") as f:
            f.write(file.getbuffer())

    st.sidebar.success("Files uploaded")


if st.sidebar.button("🔄 Rebuild Knowledge Base"):
    with st.spinner("Indexing documents..."):
        success = ingest_pdfs()

    if success:
        st.cache_resource.clear()
        st.sidebar.success("Knowledge base ready")
    else:
        st.sidebar.warning("No PDFs found")


# -----------------------
# Chat Section
# -----------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


db = load_vectordb(embeddings)

if db:
    retriever = db.as_retriever(search_kwargs={"k": 8})
else:
    retriever = None
    st.info("Upload PDFs and click 'Rebuild Knowledge Base' first.")


# Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat input
question = st.chat_input("Ask something about your documents...")

if question and retriever:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, sources = ask_question(question, retriever, llm)

            response = f"{answer}\n\n**Sources:** {', '.join(sources)}"

            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
