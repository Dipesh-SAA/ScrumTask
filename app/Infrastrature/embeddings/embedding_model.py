import os
import requests
import numpy as np
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

MODEL_NAME = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
embeddings = OpenAIEmbeddings(
    model=MODEL_NAME,
    api_key=os.getenv("OPENAI_API_KEY"),
)
API_URL = "https://vibeapp.saa.ai/DocUploadApi/api/document/GetDataInQdrant?collectionName=Global%20Scrum%20Generation%20Constitution"



def generate_embedding(text):
    return embeddings.embed_query(text)


def get_constitution_chunks():
    response = requests.get(API_URL, timeout=60)
    response.raise_for_status()

    data = response.json()
    return data["data"]


def get_chunk_text(chunk):
    return f"""Heading: {chunk.get("heading", "")}

Text:
{chunk.get("text", "")}
"""


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    if len(a) != len(b):
        raise ValueError(
            f"Vector size mismatch: user vector={len(a)}, constitution vector={len(b)}"
        )

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def rank_chunks(user_vector, chunks, top_k=5):
    ranked = []

    for chunk in chunks:
        chunk_vector = chunk.get("vectors")

        if not chunk_vector or len(user_vector) != len(chunk_vector):
            chunk_vector = generate_embedding(get_chunk_text(chunk))

        score = cosine_similarity(user_vector, chunk_vector)

        ranked.append({
            "score": float(score),
            "id": chunk["id"],
            "heading": chunk["heading"],
            "text": chunk["text"]
        })

    return sorted(ranked, key=lambda x: x["score"], reverse=True)[:top_k]


if __name__ == "__main__":
    user_input = "What are the core modules required for building an AI-native enterprise platform?"

    user_vector = generate_embedding(user_input)
    chunks = get_constitution_chunks()

    print("Embedding model:", MODEL_NAME)
    print("User vector length:", len(user_vector))
    print("Total chunks:", len(chunks))
    print("First constitution vector length:", len(chunks[0]["vectors"]))

    top_chunks = rank_chunks(user_vector, chunks, top_k=5)

    print("\nTop matching chunks:")

    for index, chunk in enumerate(top_chunks, start=1):
        print(f"\nRank {index}")
        print("Score:", chunk["score"])
        print("Heading:", chunk["heading"])
        print("Text:", chunk["text"][:300])
