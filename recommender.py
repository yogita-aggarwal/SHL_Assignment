import json


def load_catalog():

    with open("data/catalog.json", "r", encoding="utf-8") as f:
        return json.load(f)


def recommend(query):

    catalog = load_catalog()

    query = query.lower()

    results = []

    for item in catalog:

        text = (
            item.get("name", "") + " " +
            item.get("description", "")
        ).lower()

        if any(word in text for word in query.split()):
            results.append(item)

    return results[:10]