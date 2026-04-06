import faiss
import numpy as np

dimension = 512
index = faiss.IndexFlatL2(dimension)

image_map = []

def add_embedding(embedding, image_path):
    index.add(np.array([embedding]).astype("float32"))
    image_map.append(image_path)

def search_embedding(query_embedding, k=5):
    D, I = index.search(np.array([query_embedding]).astype("float32"), k)
    results = []
    for i in I[0]:
        if i < len(image_map):
            results.append(image_map[i])
    return results
