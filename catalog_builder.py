# import json

# catalog = []

# assessment = {
#     "name": "",
#     "description": "",
#     "url": "",
#     "duration": "",
#     "test_type": ""
# }

# catalog.append(assessment)

# with open("data/catalog.json", "w", encoding="utf-8") as f:
#     json.dump(catalog, f, indent=4)

# print("Catalog created!")
import json
import pickle
from catalog import catalog

# -----------------------------
# CLEAN DATA (SAFE)
# -----------------------------
clean_catalog = []

for item in catalog:
    clean_item = {
        "name": item.get("name", "").strip(),
        "link": item.get("url", "").strip(),   # normalize key name
        "tags": item.get("tags", [])
    }
    clean_catalog.append(clean_item)

# -----------------------------
# SAVE JSON (OPTIONAL)
# -----------------------------
with open("data/catalog.json", "w", encoding="utf-8") as f:
    json.dump(clean_catalog, f, indent=4)

# -----------------------------
# SAVE PICKLE (USED BY FAISS)
# -----------------------------
with open("vector_db/catalog.pkl", "wb") as f:
    pickle.dump(clean_catalog, f)

print("Clean catalog created successfully!")