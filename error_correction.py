# reflextion: Self-Correction Loop (쿼리 실행 기반 자동 보정) 
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Float,
    insert,
    inspect,
    text,
)

"""
주요 기능:
1. error 탐지: 
2: error 교정: rectify correctness of logical sql query  
"""

# sqlalchemy:
# - 파이썬 데이터베이스 ORM(Object Realtaional Mapping) 라이브러리
# - DB에 대한 CRUD 를 조작 
engine = create_engine("sqlite:///:memory:")
metadata_obj = MetaData()

# print(metadata_obj)  