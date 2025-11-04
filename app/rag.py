import os
import json
import faiss
import numpy as np
from typing import List, Dict, Tuple
from dotenv import load_dotenv
from openai import OpenAI, AzureOpenAI
from .utils import chunk_text, clean_text
from .prompts import SYSTEM_RAG, USER_RAG_TEMPLATE
from pathlib import Path

load_dotenv()
PROVIDER = os.environ.get("PROVIDER", "azure").lower()

AZURE_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")
AZURE_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_CHAT_DEPLOY = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o-mini")
AZURE_EMB_DEPLOY = os.environ.get("AZURE_OPENAI_EMBED_DEPLOYMENT", "text-embedding-3-large")

''' test sur openAI direct
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=OPENAI_KEY)
    CHAT_MODEL = "gpt-4o-mini"
    EMB_MODEL = "text-embedding-3-large"
'''


client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_version=AZURE_VERSION,
    api_key=AZURE_KEY)
CHAT_MODEL = AZURE_CHAT_DEPLOY
EMB_MODEL = AZURE_EMB_DEPLOY


CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 1200))
CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", 200))
TOP_K = int(os.environ.get("TOP_K", 4))


ROOT_DIR = Path(__file__).resolve().parents[1]
INDEX_DIR = ROOT_DIR / "index"
META_PATH = INDEX_DIR / "meta.jsonl"
FAISS_PATH = INDEX_DIR / "faiss.index"

INDEX_DIR.mkdir(parents=True, exist_ok=True)





# Rag
def embed_texts(texts: List[str]) -> np.ndarray:
    #send embeddings
    res = client.embeddings.create(input=texts, model=EMB_MODEL)
    vecs = [d.embedding for d in res.data]
    return np.array(vecs, dtype="float32")


# Index is used to retrieve easily and faster key points in texts
def load_index() -> Tuple[faiss.IndexFlatIP, List[Dict]]:

    if not (FAISS_PATH.exists() and META_PATH.exists()):
        raise FileNotFoundError("Index FAISS ou meta.jsonl introuvable. Lance ingest.py d'abord.")
    index = faiss.read_index(str(FAISS_PATH))
    with open(META_PATH, "r", encoding="utf-8") as f:
        metas = [json.loads(line) for line in f if line.strip()]
    return index, metas


#search in index
def search(query: str, k: int = TOP_K) -> List[Dict]:
    index, metas = load_index()
    q_vec = embed_texts([query])
    D, I = index.search(q_vec, k)
    results = []
    for rank, idx in enumerate(I[0]):
        if idx == -1:
            continue
        m = metas[idx]
        results.append({
            "rank": rank,
            "score": float(D[0][rank]),
            "text": m["text"],
            "source": m["source"],
            "title": m.get("title", m["source"]),
        })
    return results



# make a context out of the indexes parts ( snippets)
def build_context(snippets: List[Dict]) -> str:
    ctx_parts = []
    for s in snippets:
        ctx_parts.append(f"[Source: {s['title']}]\n" + clean_text(s["text"]))
    return "\n\n".join(ctx_parts)



# make answer with index and OpenAI answer
def answer(question: str) -> Dict:
    snippets = search(question, TOP_K)
    context = build_context(snippets)

    user_prompt = USER_RAG_TEMPLATE.format(question=question, context=context)

    chat = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_RAG},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    content = chat.choices[0].message.content

    return {
        "answer": content,
        "sources": [
            {"title": s["title"], "source": s["source"], "score": s["score"]}
            for s in snippets
        ],
    }
