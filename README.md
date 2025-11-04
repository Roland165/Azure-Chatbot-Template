# Create Your Own Chatbot with Azure (RAG Pipeline)

---

## Introduction

With the democratization of Artificial Intelligence, chatbots are now everywhere, assisting in programming, project management, customer service, or even daily tasks.  
This project demonstrates how to build your own intelligent chatbot capable of answering questions based on your own documents using Azure OpenAI models.

---

## Installation

### 1. Clone the project

```bash
git clone https://github.com/Roland165/Azure-Chatbot-Template
cd Azure-Chatbot-Template
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```
If you get an error after this command, just also tap :
  ```bash
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```
and retry the first command.

- **Mac / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the `.env` file to the project root and fill in your Azure credentials:

```env
PROVIDER="azure"

AZURE_OPENAI_ENDPOINT="https://YOUR-ENDPOINT.openai.azure.com/"
AZURE_OPENAI_API_VERSION="2024-08-01-preview"
AZURE_OPENAI_API_KEY="YOUR_API_KEY"

AZURE_OPENAI_CHAT_DEPLOYMENT="gpt-4o-mini"
AZURE_OPENAI_EMBED_DEPLOYMENT="text-embedding-3-large"

CHUNK_SIZE=800
CHUNK_OVERLAP=120
MAX_CHARS_PER_FILE=80000
MAX_TOTAL_CHUNKS=2000
```

---

## 📁 Project Structure

```
Azure-Chatbot-Template/
│
├── app/
│   ├── main.py              # FastAPI API (endpoint /ask)
│   ├── rag.py               # RAG logic (embedding, search, answering)
│   ├── prompts.py           # System and user prompts
│   └── utils.py             # Text cleaning and chunking functions
│ 
├── ui/
│    └── streamlit_app.py    # Streamlit web interface
│ 
├── data/                    # Folder containing your documents (.pdf, .txt, etc.)
│ 
├── index/                   # Automatically created folder (index + metadata)
│ 
├── ingest.py                # Document ingestion and FAISS index creation
├── .env                     # Azure environment variables
├── requirements.txt         # Python dependencies
└── README.md
```

---

## ⚙️ Run the Project

### 1. Add your documents

Place your `.pdf`, `.txt`, `.md`, or `.html` files in the folder:

```
app/data/
```

### 2. Build the FAISS index

This step reads your files, cleans them, generates embeddings, and creates a vector index.

```bash
python -m app.ingest
```

### 3. Launch the chatbot

```bash
streamlit run ui/streamlit_app.py
```

→ Then open the link displayed in your terminal (usually [http://localhost:8501](http://localhost:8501))


---

## 🧰 Tech Stack

- **Python 3.10+**
- **FastAPI** — backend API
- **Streamlit** — web interface
- **FAISS** — vector search engine
- **Azure OpenAI** — GPT-4o & text-embedding-3-large
- **PyPDF2** & **BeautifulSoup4** — file parsing utilities

---

## 💬 Author

Developed by **Roland Fontanes (EFREI Paris)**  
Personal project on AI and RAG systems.  
Powered by **Azure OpenAI**.
