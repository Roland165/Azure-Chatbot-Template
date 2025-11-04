import os
import json
import glob
import numpy as np
import faiss
from pathlib import Path
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from app.utils import chunk_text, clean_text
from app.rag import embed_texts, INDEX_DIR, META_PATH, FAISS_PATH, CHUNK_SIZE, CHUNK_OVERLAP

load_dotenv()

# Limits for optimization
MAX_CHARS_PER_FILE = int(os.environ.get("MAX_CHARS_PER_FILE", "80000"))
ALLOWED_EXTS = {".txt", ".md", ".pdf", ".html"}

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
os.makedirs(str(INDEX_DIR), exist_ok=True)


# Function to read the text in the files in the data folder
def read_text_from_file(path: str) -> str:


    ext = os.path.splitext(path)[1].lower()
    if ext not in ALLOWED_EXTS:
        return ""

    if ext in [".txt", ".md" ]:
        text = open(path, "r", encoding="utf-8", errors="ignore").read()
    elif ext == ".html":
        html = open(path, "r", encoding="utf-8", errors="ignore").read()
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ")

    elif ext == ".pdf":


        from PyPDF2 import PdfReader
        text_chunks = [ ]
        reader = PdfReader(path )
        for page in reader.pages:

            try:
                t = page.extract_text() or ""
                if t:
                     text_chunks.append(t)

            except Exception:
                pass
        text = "\n".join(text_chunks)

    else:
        text = ""
    return text[:MAX_CHARS_PER_FILE]


def main():
    # get all files
    files = sorted(glob.glob(str(DATA_DIR / "**/*"), recursive=True))

    chunks = []
    metas = []

    # clean and split into chunks each files in /data
    for f in files:
        if os.path.isdir(f):
            continue

        raw = read_text_from_file(f)
        if not raw.strip():
            continue

        title = os.path.basename(f)
        clean = clean_text(raw)
        print(f"[INGEST] {title} → {len(clean)} chars")


        #splitting cleaned text into chunks

        for ch in chunk_text(clean, CHUNK_SIZE, CHUNK_OVERLAP):
            if len(chunks) >= MAX_TOTAL_CHUNKS:
                break
            metas.append({"source": f, "title": title, "text": ch})
            chunks.append(ch)

    if not chunks:
        print("No document. Please add files in ./data !")
        return


    vecs = embed_texts(chunks).astype("float32")

    #index part
    faiss.normalize_L2(vecs )
    index = faiss.IndexFlatIP( vecs.shape[1])
    index.add(vecs)


    os.makedirs(str(INDEX_DIR), exist_ok=True)
    faiss.write_index(index, str(FAISS_PATH))

    with open(str(META_PATH), "w", encoding="utf-8") as w:
        for m in metas:
            w.write(json.dumps(m, ensure_ascii=False) + "\n")

    print(f"Index build: {len(chunks)} chunks → {str(FAISS_PATH)}")







if __name__ == "__main__":
    main()
