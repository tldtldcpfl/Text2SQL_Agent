from langchain_community.utilities import SQLDatabase

# NOTE: context 필터링 기준 정의 필요 (예: 테이블명, 컬럼명, 데이터 샘플 등)
  
# db 연결 
def connect_db(db_path):
    """SQLite 데이터베이스에 연결하여 SQLDatabase 인스턴스 반환"""
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    return db

db = connect_db("Chinook.db") 