import ollama
from neo4j import GraphDatabase
from pathlib import Path
from kg.utils.parse import refine_path_for_llm 
from kg.retrieve_kg import retrieve_logical_paths, extract_query_entities
import json 
import re

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.json"

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

def contains_chinese(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))

# logical_context 기반 최종 답변 생성
def logical_answer_generate(

    query:str,

    logical_context:str
):
    # graph-oriented prompt 
    prompt = f"""
아래 그래프 경로만 근거로 질문에 답하세요.

[논리 그래프 경로]
{logical_context} 

[질문] 
{query}

[답변 규칙]

- 반드시 한국어 문장으로만 답하세요.
- 중국어 단어, 중국어 문장, 한자를 사용하지 마세요.
- 영어 질문이 들어와도 답변은 한국어로 번역해서 설명하세요.
- 그래프 관계에 근거한 인과 흐름을 단계적으로 설명하세요.
- 그래프에 없는 내용은 추측하지 마세요.
""" 

    response = ollama.chat(

        model=config['llm_id'],

        messages=[
            {
                "role": "system",
                "content": (
                    "당신은 한국어로만 답하는 인과 추론 도우미입니다. "
                    "모든 출력은 반드시 한국어 한글 문장이어야 합니다. "
                    "중국어와 한자는 절대 사용하지 마세요."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        options={
            "temperature": 0.2
        }
    )

    answer = response[
        "message"
    ]["content"]

    if not contains_chinese(answer):
        return answer

    retry_prompt = f"""
이전 답변에 중국어 또는 한자가 포함되어 있어 사용할 수 없습니다.
아래 내용을 반드시 한국어 한글 문장으로만 다시 작성하세요.

[질문]
{query}

[논리 그래프 경로]
{logical_context}

[금지]
- 중국어 사용 금지
- 한자 사용 금지
- 영어로 답변 금지
"""

    retry_response = ollama.chat(

        model=config['llm_id'],

        messages=[
            {
                "role": "system",
                "content": "오직 한국어 한글 문장으로만 답하세요. 중국어와 한자는 절대 출력하지 마세요."
            },
            {
                "role": "user",
                "content": retry_prompt
            }
        ],

        options={
            "temperature": 0
        }
    )

    return retry_response[
        "message"
    ]["content"]


def gen_kg_answer(user_query: str): 
    entities = extract_query_entities(user_query) 
    print('[debug] 추출된 엔티티: ', entities)  
    logical_paths = retrieve_logical_paths(entities)
    # print('debug: logical_paths\n', logical_paths)
    context_triplet = refine_path_for_llm(logical_paths) 
    # print('[retrieved kg]\n', context_triplet)  
    # 이어진 문장 형태로 concat 
    logical_context = "\n".join(context_triplet)  
    # finally, gen the answer   
    logical_answer = logical_answer_generate(user_query, logical_context)
    return logical_answer

# user_query = "Why does Dense Retriever cause retrieval failure?"
# print(logical_answer)          
