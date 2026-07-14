<div align="center">

# 📄 PDF Chatbot with Groq + FAISS

**Chat with your PDFs using blazing-fast Groq LLMs and FAISS vector search**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM%20API-F55036)](https://groq.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Streamlit-based PDF Q&A application that uses **LangChain**, **FAISS vector search**, and the **Groq API** to let you have intelligent conversations with any PDF document.

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 📤 **Upload PDFs** | Process any PDF document in seconds |
| 🔍 **Vector Search** | Fast, accurate semantic search powered by FAISS |
| 🤖 **AI-Powered Answers** | Intelligent, context-aware responses via Groq LLMs |
| 💬 **Chat History** | Full conversation history tracked in-session |
| ⚡ **Multiple LLM Models** | Switch between different Groq models on the fly |
| 📚 **Source Transparency** | View the exact retrieved chunks behind every answer |

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌────────────────────┐
│  PDF Upload │ ──▶ │  Text Splitting   │ ──▶ │  HuggingFace        │
│  (PyPDF)    │     │  (Recursive       │     │  Embeddings         │
│             │     │   Char Splitter)  │     │                     │
└─────────────┘     └──────────────────┘     └─────────┬───────────┘
                                                          ▼
┌─────────────┐     ┌──────────────────┐     ┌────────────────────┐
│  Answer +   │ ◀── │  Groq LLM         │ ◀── │  FAISS Vector       │
│  Sources    │     │  (Multi-model)    │     │  Store              │
└─────────────┘     └──────────────────┘     └────────────────────┘
```

| Component | Technology |
|---|---|
| PDF Loader | `PyPDF` |
| Text Splitter | Recursive character-based chunking |
| Embeddings | HuggingFace `sentence-transformers` |
| Vector Store | `FAISS` |
| LLM | Groq API (multiple model options) |
| UI | Streamlit |

---

## 🚀 Quick Start

### Local Setup

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd pdf-chatbot
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set your Groq API key**
```bash
export GROQ_API_KEY="your_groq_api_key"      # On Windows: set GROQ_API_KEY=your_groq_api_key
```

**5. Run the app**
```bash
streamlit run app.py
```

The app will open at **`http://localhost:8501`** 🎉

---

## ☁️ Deployment on Streamlit Cloud

### Prerequisites
- ✅ GitHub account
- ✅ [Streamlit Cloud](https://share.streamlit.io) account (free)
- ✅ Groq API key

### Steps

**1. Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

**2. Deploy on Streamlit Cloud**
- Go to [Streamlit Cloud](https://share.streamlit.io)
- Click **"New app"**
- Select your repository, branch, and main file (`app.py`)
- Click **"Deploy"**

**3. Add your Secrets**
- After deployment, go to the app's **Settings → Secrets**
- Add your Groq API key:
```toml
GROQ_API_KEY = "your_groq_api_key"
```

---

## 📖 Usage

1. **Upload a PDF** — Use the file uploader in the sidebar
2. **Wait for Processing** — The app extracts and indexes the document
3. **Ask Questions** — Type your question in the chat input
4. **View Answers** — Get AI-generated answers based on the PDF content
5. **See Retrieved Chunks** — Expand the source panel to inspect the exact context used

---

## 📋 Requirements

- Python **3.9+**
- See [`requirements.txt`](requirements.txt) for the full dependency list

## 🔑 API Keys Required

| Key | Where to get it |
|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).


---

<div align="center">

Made with ❤️ using Streamlit, LangChain, FAISS, and Groq

</div>
