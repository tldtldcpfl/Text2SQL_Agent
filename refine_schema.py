from langchain_community.utilities import SQLDatabase
from sqlalchemy import inspect 
from langchain_community.embeddings import OllamaEmbeddings
import numpy as np

def full_table_schema():
    """전체 테이블 명, 컬럼 명, 외래 키 정보 출력"""
    # db 연결
    db = SQLDatabase.from_uri("sqlite:///Chinook.db") 

    # SQLAlchemy의 inspect 함수를 사용하여 데이터베이스의 메타데이터를 검사하는 객체 생성 
    inspector = inspect(db._engine) # db는 SQLDatabase 객체

    schema_structure = {}
    for table in inspector.get_table_names():
        schema_structure[table] = {
            "columns": [c['name'] for c in inspector.get_columns(table)],
            "foreign_keys": [f['referred_table'] for f in inspector.get_foreign_keys(table)]
        }

    # 세부 목표: llm 주입에 적합한 구조화된 테이블 컨텍스트 생성 
    # table docs 생성 - 테이블 이름, 컬럼, 외래키 정보를 포함하는 문자열 리스트 생성  
    table_docs = [
        f"Table: {t_name}, Columns: {data['columns']}, Foreign Keys: {data['foreign_keys']}" 
        for t_name, data in schema_structure.items() 
    ]
    # print('[info] This is full table schema, not allowed to feed it to llm directly.') 
    return table_docs  

table_docs = full_table_schema() 
# print(table_docs)  

