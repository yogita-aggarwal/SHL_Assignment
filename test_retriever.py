from retriever import search_catalog

results = search_catalog("Python developer with SQL skills")

for item in results:
    print(item)