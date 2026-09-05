import chromadb
from sentence_transformers import SentenceTransformer
import json

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()

collection = client.create_collection("attack_techniques")


def load_attack_data(json_path: str, limit: int = 300):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0

    for obj in data.get("objects", []):
        if obj.get("type") == "attack-pattern":

            name = obj.get("name", "")
            description = obj.get("description", "")

            if not description:
                continue

            embedding = embedding_model.encode(description).tolist()

            collection.add(
                ids=[obj.get("id", str(count))],
                embeddings=[embedding],
                documents=[description],
                metadatas=[{"technique_name": name}]
            )

            count += 1

            if count >= limit:
                break

    print(f"Loaded {count} ATT&CK techniques into ChromaDB.")


def retrieve_technique(query: str, top_k: int = 3):

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    matches = []

    for i in range(len(results["ids"][0])):

        matches.append({
            "technique_name":
                results["metadatas"][0][i]["technique_name"],

            "description":
                results["documents"][0][i][:150] + "..."
        })

    return matches