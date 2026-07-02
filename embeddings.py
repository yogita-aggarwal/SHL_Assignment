import json
import pickle
from sentence_transformers import SentenceTransformer
import faiss

# Load model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def build_embeddings():

    with open("data/catalog.json", "r", encoding="utf-8") as f:
        catalog = json.load(f)

    texts = []

    for item in catalog:

        text = (
            item["name"] + " " +
            item["description"]
        )

        texts.append(text)

    embeddings = model.encode(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])

    index.add(embeddings)

    faiss.write_index(index, "vector_db/catalog.index")

    with open("vector_db/catalog.pkl", "wb") as f:

        pickle.dump(catalog, f)

    print("Embeddings created successfully!")


if __name__ == "__main__":
    build_embeddings()