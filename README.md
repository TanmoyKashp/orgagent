**Development Log** : https://docs.google.com/document/d/1wvHRMUD---UzLe-KYKYgBOkAHmzGuqjlIq63jBLAzkA/edit?usp=sharing

# OrgAgent

**OrgAgent** is a high-performance, cloud-integrated AI assistant designed to provide accurate answers based on your organization's document database. 

Formerly a local-only project, OrgAgent now leverages infrastructure for superior speed, scalability, and model variety.


### 🛠 Built With
* **OpenRouter**: Access to top-tier models like DeepSeek-R1, GPT-4o, and Claude 3.5.
* **Pinecone**: Serverless Cloud Vector Database for high-speed retrieval.
* **LangChain**: The backbone for RAG orchestration.
* **OpenAI Embeddings**: High-dimensional vectorization for precise semantic search.

---

## Features

*  **Advanced Reasoning**: Powered by the latest models like DeepSeek-R1 via OpenRouter.
*  **Cloud Vector Storage**: Uses Pinecone for persistent, scalable document retrieval.
*  **Context-Aware RAG**: Uses a strict retrieval-augmented generation loop to minimize hallucinations.
*  **Multi-PDF Support**: Automatic ingestion and chunking of organizational PDF files.
*  **Precision Embeddings**: Utilizes `text-embedding-3-large` (3072 dimensions) for superior search accuracy.

---

## What's Changed?

| Feature | Old Version (Local) | New Version (Cloud-Hybrid) |
| :--- | :--- | :--- |
| **LLM** | Ollama (Llama 3) | **OpenRouter (DeepSeek-R1-Chimera)** |
| **Vector DB** | Chroma (Local Folder) | **Pinecone (Cloud Serverless)** |
| **Embeddings** | Nomic (Local) | **OpenAI Large (via OpenRouter)** |
| **Persistence** | Local `vectordb/` | **Cloud Managed** |
| **Dimensions** | 768 | **3072 (Higher accuracy)** |

---
