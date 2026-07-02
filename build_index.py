import faiss
import pickle
from sentence_transformers import SentenceTransformer
from catalog import catalog

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []
clean_catalog = []

for item in catalog:
    texts.append(item["name"] + " " + " ".join(item["tags"]))

    clean_catalog.append({
        "name": item["name"],
        "link": item["url"],
        "tags": item["tags"]
    })

embeddings = model.encode(texts)
dim = embeddings.shape[1]

index = faiss.IndexFlatL2(dim)
index.add(embeddings)

faiss.write_index(index, "vector_db/catalog.index")

with open("vector_db/catalog.pkl", "wb") as f:
    pickle.dump(clean_catalog, f)

print("FAISS index built successfully")