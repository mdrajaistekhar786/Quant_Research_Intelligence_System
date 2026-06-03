import numpy as np
import faiss
import os
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer
import pickle
from pathlib import Path

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Embedding model
embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

# Load FAISS index
index = faiss.read_index(
    str(BASE_DIR / "data" / "vector_store" / "faiss_index.bin")
)

# Load chunks
with open(
    BASE_DIR / "data" / "hybrid_candidates.pkl",
    "rb"
) as f:
    chunks = pickle.load(f)

# Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def retrieve(query, top_k=5):
    query_embedding = embedding_model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:
        if idx < len(chunks):
            results.append(chunks[idx])

    return results


def build_context(results):
    context = ""

    for i, chunk in enumerate(results):
        context += f"\n\nDocument {i+1}:\n"

        if isinstance(chunk, dict):
            if "text" in chunk:
                context += chunk["text"]
            elif "chunk" in chunk:
                context += str(chunk["chunk"])
            else:
                context += str(chunk)
        else:
            context += str(chunk)

    return context


def generate_answer(question, context):
    prompt = f"""
You are a quantitative finance research assistant.

Use the provided context to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content