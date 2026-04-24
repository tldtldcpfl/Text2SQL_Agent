from langchain_community.utilities import SQLDatabase

# db 연결 
# SQLite 데이터베이스 파일에서 SQLDatabase 인스턴스 생성
# 실습에 활용할 chinook 데이터베이스를 다운로드 
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

# DB dialect 출력(sqlite)
# print(db.dialect)

# 데이터베이스에서 사용 가능한 테이블 이름 목록 출력
print(db.get_usable_table_names())

# SQL 쿼리 실행
db.run("SELECT * FROM Artist LIMIT 5;")

context = db.get_context()
# print(context)

# 전체 context가 너무 길어서 일부만 피딩 (전체 피딩시 api 호출 비용 폭탄)  
# context 필터링 기준: 
print(context['table_names'])