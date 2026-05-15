# Entrypoint of the application 
import warnings
warnings.filterwarnings("ignore")
from prompt import system_prompt 
from emb_query import emb_sim
from gen_sql import generate_sql, extract_sql 
from run_sql import execute_sql
import json 
with open('config.json', 'r') as f:
    config = json.load(f)

# ollama 엔드포인트: ollama는 로컬에서 실행되는 LLM 서버
OLLAMA_URL = "http://localhost:11434/api/generate"

def main(user_query):
    """
    add description of main function here    
    """

    # SQL 생성/정제/실행 
    df = execute_sql(user_query, config['llm_id'], system_prompt) 
    print('[info] table results:\n', df)

# Enry point of the program 
if __name__ == "__main__":
    # NOTE: while문으로 멀티 턴 유저 쿼리받도록 수정 필요 (현재는 싱글 턴)  
    # user_query = input("자연어 질문을 입력하세요: ")  # 사용자로부터 자연어 질문 입력 받기
    # from emb_query import user_query  
    
    # 멀티턴 유저 입력 받기
    user_query = input("자연어 질문을 입력하세요 (종료하려면 'exit' 입력): ")
    while user_query.lower() != 'exit':
        main(user_query)  # 입력된 질문으로 main 함수 실행
        user_query = input("자연어 질문을 입력하세요 (종료하려면 'exit' 입력): ")
    print("프로그램을 종료합니다.")     