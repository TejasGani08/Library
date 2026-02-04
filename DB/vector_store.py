import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim=1536):
        self.index = faiss.IndexFlatL2(dim)
        self.vectors = []
        self.metadata = []

    def add(self, embedding, metadata):
        vec = np.array([embedding]).astype("float32")
        self.index.add(vec)
        self.vectors.append(vec)
        self.metadata.append(metadata)

    def search(self, query_embedding, top_k=3):
        vec = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(vec, top_k)
        results = []
        for i in indices[0]:
            if i < len(self.metadata):
                results.append(self.metadata[i])
        return results