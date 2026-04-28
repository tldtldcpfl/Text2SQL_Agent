import ollama 
from prompt import system_prompt
import time
from config import llm_id  

# 주요 기능: llm의 sql 쿼리문 생성 (validator 넘기기 전)

def generate_sql(user_query, llm_id, system_prompt):

    # ollama API 호출 
    response = ollama.chat(model=llm_id, 
                        messages=[{"role": "system", "content": system_prompt},
                                    {"role": "user", "question": user_query}
                                    ],
                            options={
                                "temperature": 0,  # 0으로 설정하면 결정록적(일관적) 응답 유도
                                "num_predict": 500. # 출력 길이 제한 (서술형 응답 최소화)
                            }             
                            )

    # 구조화 & 유사도 기반 정제된 context가 주입된 쿼리 생성
    # print(response['message']['content'])
    gen_sql = response['message']['content'] 
    return gen_sql    
 
def infer_speed_llm(model_id, user_query):
    """ollama 내 llama.cpp가 제공하는 고성능 추론 최적화 기술 (gguf 양자화) 사용"""
    # 추론 속도 측정 
    start_time = time.perf_counter()

    generate_sql(model_id, user_query, system_prompt) 

    end_time = time.perf_counter()
    print(f"응답 시간: {end_time - start_time:.2f}초") 

# 추론 속도 가속화 
# model_id = "qwen2.5:7b-instruct-q4_k_m"
# infer_speed_llm(model_id)   # 2.65s  

def extract_sql(gen_sql):
    """마크다운 코드 블록에서 순수 SQL만 추출"""
    # ```sql ... ``` 패턴으로 SQL 추출
    import re 
    sql_match = re.search(r"```sql\s*(.*?)\s*```", gen_sql, re.DOTALL)
    
    if sql_match:
        return sql_match.group(1).strip()
    
    # 코드 블록이 없으면 전체 내용 반환
    return gen_sql.strip()

# 테스트 코드 
# user_query = "artist name이 'AC/DC'인 album의 title과 id를 알려줘" 
# gen_sql = generate_sql(user_query, llm_id, system_prompt)  
# print('[info] generated sql before cleaning:\n',gen_sql) 
# clean_sql = extract_sql(gen_sql)  
# print('[info] cleaned sql:\n',clean_sql) 