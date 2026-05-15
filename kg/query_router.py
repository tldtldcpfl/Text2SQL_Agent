import numpy as np
import warnings
warnings.filterwarnings('ignore')
from sentence_transformers import SentenceTransformer, util

# encoder for query routing 
enc = SentenceTransformer(
        "BAAI/bge-m3"
    )   

# 각 클래스를 대표하는 'Anchor(기준) 텍스트' 정의
class_anchors = {
    "semantic": "What is, definition, explanation, general info, concept",
    "logical": "Why, cause, reason, lead to, impact, depend on, result in, causal relationship",
    "hybrid": "Comparison, detailed analysis, multi-step process, complex relationship"
}

# instruction
instruction = "Represent this query for intent classification to identify causal or logical reasoning: "

def classify_query(user_query):
    # 쿼리 및 앵커 임베딩 생성
    query_emb = enc.encode(instruction + user_query)
    anchor_embs = enc.encode(list(class_anchors.values()))
    
    # 유사도 계산
    probs = util.cos_sim(query_emb, anchor_embs).numpy()[0]
    
    # Softmax를 적용하여 확률값으로 변환 (선택 사항)
    exp_probs = np.exp(probs)
    normalized_probs = exp_probs / np.sum(exp_probs)
    
    return {
        "Semantic_prob": normalized_probs[0],
        "Logical_prob": normalized_probs[1],
        "Hybrid_prob": normalized_probs[2]
    } 

# user_query = "Why does Dense Retriever cause retrieval failure?"
# query_type =classify_query(user_query)      
# print(query_type) 