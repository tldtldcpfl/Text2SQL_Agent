# main.py  
import requests 
import json 
from prompt import system_prompt 
from emb_query import emb_sim
from config import emb_id, llm_id
from gen_sql import generate_sql, extract_sql 
from run_sql import display_df

# ollama 엔드포인트: ollama는 로컬에서 실행되는 LLM 서버
OLLAMA_URL = "http://localhost:11434/api/generate"

def main(user_query):
    """
    add description of main function here    
    """

    # SQL 생성: LLM에 시스템 프롬프트와 유사 스키마를 함께 전달하여 SQL 생성
    gen_sql = generate_sql(llm_id, system_prompt)
    clean_sql = extract_sql(gen_sql)  # 마크다운 코드 블록에서 SQL만 추출 
    print('[info] cleaned sql:\n',clean_sql)

    # SQL 실행: db 쿼리 실행 결과
    df = display_df(clean_sql) 
    print('[info] table results:\n', df)


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
    
    # main(user_query)   