# 🧠 OrgAgent

OrgAgent is a local, privacy-first AI assistant that answers questions using your organization's documents.

Built with:
- Ollama (local LLM)
- LangChain
- Chroma Vector DB
- Streamlit UI

---

## 🚀 Features

✅ Multi-PDF ingestion  
✅ Local embeddings (nomic-embed-text)  
✅ Local LLM answering (llama3)  
✅ Admin panel for document upload  
✅ Client chat interface  
✅ No internet/API costs  
✅ Fully offline + private  

---

## 📦 Setup

### 1. Clone repo
git clone https://github.com/TanmoyKashp/orgagent.git
cd orgagent

### 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Install Ollama models
ollama pull llama3:8b
ollama pull nomic-embed-text

---

## ▶️ Run

### Terminal 1
ollama serve

### Terminal 2
streamlit run app/ui.py

Open:
http://localhost:8501

---

## 📁 Structure

app/
  ui.py       → client chat UI
  ingest.py   → document ingestion
  rag.py      → CLI testing
  pages/      → admin panel

uploads/      → PDFs
vectordb/     → embeddings DB

---

## 🧩 Future Roadmap

- Role-based access
- Multi-tenant support
- Authentication
- Docker deployment
- Cloud hosting

---

Built by Tanmoy Kashyap
