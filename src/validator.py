# 주요 기능: llm이 생성한 sql 쿼리문 검증 (구문, 논리, 보안 레벨) 
import warnings
warnings.filterwarnings('ignore') 
from gen_sql import generate_sql, llm_id
from prompt import system_prompt 

sql_query = generate_sql(llm_id, system_prompt)
print(sql_query) 

"""
sql 쿼리 검증:
- 구문 레벨: select, update, delete, insert 구문 등 키워드 확인
- 논리 레벨: where 절의 조건문, join 절의 테이블 관계 등 논리적 오류 확인
- 보안 레벨: 민감한 데이터(테이블명, 컬럼명) 접근 제한  
"""

sql_upper =  sql_query.upper().strip() 
print('[info] Generated SQL Query:\n', sql_query)

# 허용된 sql 구문 키워드 
allowed_keywords = ["SELECT", "INSERT", "UPDATE", "WITH", 'FROM', 'WHERE', 'JOIN', 'GROUP BY', 'ORDER BY', 'LIMIT'] 
# 구문 레벨 검증
if not any(sql_upper.startswith(keyword) for keyword in allowed_keywords):
    print("[error] 허용되지 않은 SQL 구문입니다.")  

# drop, truncate같은 위험한 명령어 차단 
dangerous_keywords = ["DROP", "TRUNCATE", "ALTER", "DELETE"]
if any(keyword in sql_upper for keyword in dangerous_keywords):
    print(f"[error] 허용되지않는 SQL 명령어가 포함되어 있습니다: {', '.join(dangerous_keywords)}")  

