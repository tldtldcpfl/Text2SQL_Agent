from langchain_community.embeddings import OllamaEmbeddings
import numpy as np
from refine_schema import table_docs
import warnings
warnings.filterwarnings('ignore') 
from config import emb_id  

def emb_sim(emb_id, top_k, user_query):

    # 임베딩 모델 호출 
    embedding_model = OllamaEmbeddings(model= emb_id) 

    # table_docs와 user_query 간 유사도 계산  
    # album 테이블과 artist 테이블을 조인해서 atist name에 해당하는 album title과 album id를 리턴하는 유저 쿼리
    user_query = "artist name이 'AC/DC'인 album의 title과 id를 알려줘"
    # user query 임베딩
    query_emb = embedding_model.embed_query(user_query)
    # table_docs 임베딩
    schema_emb = embedding_model.embed_documents(table_docs)

    # 질문과 테이블 설명 간의 코사인 유사도 계산
    # embedding_model로 user_query와 table_docs 간 유사도 계산을 위한 두 벡터 내적 
    sim_score = np.array(query_emb) @ np.array(schema_emb).T

    # 유사도 기반으로 내림차순 정렬 (인덱스 반환)
    top_indices = np.argsort(sim_score)[::-1][:top_k]
    # 상위 K개 테이블 데이터 추출
    top_tables = [table_docs[i] for i in top_indices]
    return top_tables 

user_query = "artist name이 'AC/DC'인 album의 title과 id를 알려줘" 
top_tables = emb_sim(emb_id, 3, user_query)
# print(top_tables)  