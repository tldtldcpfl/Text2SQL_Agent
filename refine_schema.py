from langchain_community.utilities import SQLDatabase
from sqlalchemy import inspect 

# db 연결 
# SQLite 데이터베이스 파일에서 SQLDatabase 인스턴스 생성
# 실습에 활용할 chinook 데이터베이스를 다운로드 
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# DB dialect 출력(sqlite)
print(db.dialect)

# 데이터베이스에서 사용 가능한 테이블 이름 목록 출력
# print('[info] db 내 table name 출력:\n', db.get_usable_table_names())

# SQL 쿼리 실행
# db.run("SELECT * FROM Artist LIMIT 5;")

# db 메타데이터 read
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

print(table_docs)  
