import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("Step 1: Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Step 2: Model loaded!")

print("Step 3: Loading knowledge base...")

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    knowledge = json.load(f)

print("Step 4: Knowledge base loaded!")

documents = [
    f"{item['query']} | {item['issue']} | {item['solution']}"
    for item in knowledge
]

print("Step 5: Creating embeddings...")

embeddings = model.encode(documents)

print("Step 6: Embeddings created!")

# Convert embeddings to float32 for FAISS
embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

# Create FAISS index
index = faiss.IndexFlatL2(dimension)

# Add embeddings to index
index.add(embeddings)

print("✅ RAG Engine Ready!")

# ==========================================================
# Search Similar Incidents
# ==========================================================

def search_similar_incidents(query, top_k=3):
    """
    Search for semantically similar incidents using FAISS.
    Returns the top_k similar incidents along with similarity scores.
    """

    # Generate embedding for incoming query
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    # Search FAISS index
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for rank, idx in enumerate(indices[0]):

        distance = float(distances[0][rank])

        # Convert L2 distance to an easy-to-read similarity score
        similarity = max(0, 100 - (distance * 10))

        incident = knowledge[idx].copy()
        incident["similarity"] = round(similarity, 2)
        incident["distance"] = round(distance, 4)

        results.append(incident)

    return results