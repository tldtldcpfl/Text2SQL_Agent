import warnings
warnings.filterwarnings('ignore') 
from gen_sql import generate_sql, llm_id
from prompt import system_prompt 
from db_connect import db   
import re 
import pandas as pd 

# 주요 기능: validator 검증을 통과한 sql 쿼리를 db에 실행

def extract_sql(gen_sql):
    """마크다운 코드 블록에서 순수 SQL만 추출"""
    # ```sql ... ``` 패턴으로 SQL 추출
    sql_match = re.search(r"```sql\s*(.*?)\s*```", gen_sql, re.DOTALL)
    
    if sql_match:
        return sql_match.group(1).strip()
    
    # 코드 블록이 없으면 전체 내용 반환
    return gen_sql.strip()

# 데이터를 표 형태로 변환
def display_df(clean_sql):
    db_result = db.run(clean_sql)
    import ast
    db_list = ast.literal_eval(db_result) 
    df = pd.DataFrame(db_list, columns=["앨범명","아티스트명" ,"앨범 ID"])
    return df.head(10)

gen_sql = generate_sql(llm_id, system_prompt)
clean_sql = extract_sql(gen_sql)
df = display_df(clean_sql)  
print(df)   
