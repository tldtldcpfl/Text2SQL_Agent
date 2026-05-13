import ollama
from neo4j import GraphDatabase
from utils.parse import refine_path_for_llm 
from retrieve_kg import retrieve_logical_paths, extract_query_entities
import json 
with open('config.json', 'r') as f:
    config = json.load(f)

# logical_context 기반 최종 답변 생성
def logical_answer_generate(

    query,

    logical_context
):

    prompt = f"""
You are a causal reasoning assistant.

Use the logical graph paths
to explain the reasoning chain.

[Logical Graph Context]

{logical_context} 

[Question]

{query}

Requirements: 

- Explain step-by-step causal flow 
- Use logical reasoning 
- Avoid hallucination 
- Ground answer only on graph relations
""" 

    response = ollama.chat(

        model=config['llm_id'],

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        options={
            "temperature": 0.2
        }
    )

    return response[
        "message"
    ]["content"] 


def gen_kg_answer(user_query: str): 
    entities = extract_query_entities(user_query) 
    logical_paths = retrieve_logical_paths(entities)
    context_triplet = refine_path_for_llm(logical_paths) 
    logical_context = "\n".join(context_triplet) 
    # finally, gen the answer   
    logical_answer = logical_answer_generate(user_query, logical_context)
    return logical_answer

user_query = "Why does Dense Retriever cause retrieval failure?"
# print(logical_answer)          