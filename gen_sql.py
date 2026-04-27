import ollama 
from prompt import system_prompt
from emb_query import user_query
import time

# 주요 기능: llm의 sql 쿼리문 생성 (validator 넘기기 전)


# llm congig   
# llm_id = "qwen3.5:latest"
llm_id = "qwen2.5:7b-instruct-q4_K_M" 

def generate_sql(llm_id, system_prompt):

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
    print(response['message']['content'])
    gen_sql = response['message']['content'] 
    return gen_sql    

# gen_sql = generate_sql(llm_id, system_prompt)  
# print(gen_sql) 
 
def infer_speed_llm(model_id):
    # 추론 속도 측정 
    start_time = time.perf_counter()

    generate_sql(model_id, system_prompt) 

    end_time = time.perf_counter()
    print(f"응답 시간: {end_time - start_time:.2f}초") 

# 추론 속도 가속화 
# ollama 내 llama.cpp가 제공하는 고성능 추론 최적화 기술 (gguf 양자화) 사용
model_id = "qwen2.5:7b-instruct-q4_k_m"
infer_speed_llm(model_id)   # 2.65s 