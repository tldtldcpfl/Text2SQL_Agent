# 주요 기능: validator 검증을 통과한 sql 쿼리를 db에 실행 
import warnings
warnings.filterwarnings('ignore') 
from gen_sql import generate_sql
from config import llm_id 
from prompt import system_prompt 
from db_connect import db   
import pandas as pd 
from gen_sql import extract_sql 

# 데이터를 표 형태로 변환
def display_df(clean_sql):
    # clean 쿼리 db 실행
    db_result = db.run(clean_sql)
    import ast 
    db_list = ast.literal_eval(db_result) 
    columns = clean_sql.split("SELECT")[1].split("FROM")[0].strip().split(",")
    columns = [col.strip() for col in columns]  # 컬럼명 공백 제거
    df = pd.DataFrame(db_list, columns=columns) 
    # df의 top 10 출력 
    return df.head(10) 

gen_sql = generate_sql(llm_id, system_prompt)
clean_sql = extract_sql(gen_sql) 
df = display_df(clean_sql)   
# print(df)      