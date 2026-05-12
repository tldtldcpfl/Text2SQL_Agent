# vector index 구축
from sentence_transformers import SentenceTransformer
import faiss # ann search 
import numpy as np
import json 

with open('config.json', 'r') as f:
    config = json.load(f) 


# vector index 구축
from sentence_transformers import SentenceTransformer
import faiss # ann search 
import numpy as np

def add_index(docs: list):
    "문서 집합 인코딩 이후 faiss index에 적재"
    # embedding model
    embed_model = SentenceTransformer(
        "BAAI/bge-m3"
    )
    # embedding
    doc_embeddings = embed_model.encode(
        docs,  # 문서 집합 
        normalize_embeddings=True
    )

    # faiss index
    dimension = doc_embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        np.array(doc_embeddings).astype("float32")
        )     # type: ignore

# with open(config['faiss_doc_path'], 'r') as f:
#     docs = json.load(f)

# add_index(docs)   