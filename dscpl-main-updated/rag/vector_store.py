# rag/vector_store.py

import os
import json
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

def create_vector_store(json_path="rag/socialverse_data.json", save_path="rag/faiss_index"):
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    posts = raw_data.get("posts", []) or raw_data.get("data", [])
    docs = []

    print(f"🔍 Total posts found: {len(posts)}")

    for idx, post in enumerate(posts):
        summary_obj = post.get("post_summary", {})
        if isinstance(summary_obj, dict):
            title = summary_obj.get("title", "").strip()
            desc = summary_obj.get("description", "").strip()

            if desc:
                full_text = f"{title}\n\n{desc}" if title else desc
                docs.append(Document(page_content=full_text))

    if not docs:
        raise ValueError("[!] No valid documents to embed.")

    print(f"🧠 Embedding {len(docs)} documents with HuggingFace...")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(docs, embeddings)

    os.makedirs(save_path, exist_ok=True)
    vector_store.save_local(save_path)
    print(f"[✓] FAISS index saved to {save_path}")
