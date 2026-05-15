import ollama
from neo4j import GraphDatabase
from pathlib import Path
from kg.utils.parse import refine_path_for_llm 
from kg.utils.parse import parse_entity_response
from kg.utils.stop_words import ENTITY_STOPWORDS
import json 
import re

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.json"

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# grpah db driver  
driver = GraphDatabase.driver(
    # NEO4J_URI
    config['neo4j_url'],

    # config: user/pw 
    auth=(
        config['neo4j_user'],
        config['neo4j_password']
    )
) 

def fallback_extract_entities(query):
    """LLM이 유저 쿼리에서 엔티티를 빈 리스트로 반환할 시 stop_words를 제외한 단어를 유저 쿼리에서 재추출한다."""
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9_-]*|[가-힣]+", query.lower())
    content_tokens = [
        token
        for token in tokens
        if token not in ENTITY_STOPWORDS and len(token) > 1
    ]

    candidates = []

    for size in range(min(3, len(content_tokens)), 0, -1):
        for idx in range(0, len(content_tokens) - size + 1):
            candidate = " ".join(content_tokens[idx:idx + size])
            if candidate not in candidates:
                candidates.append(candidate)

    return candidates

def extract_query_entities( 
    query 
):
    "llm extracts entities from user query" 

    system_prompt = """
You extract entity names for Neo4j Knowledge Graph retrieval.

Rules:
- The Knowledge Graph stores entity names in English.
- Return only a valid JSON array of strings.
- Do not include markdown, explanations, labels, or code fences.
- Return short English noun phrases that could match graph node names.
- If the user query is Korean, translate only the entity concepts into English.
- Remove intent/relation words such as why, cause, caused, reason, effect, result, depend, 원인, 이유.
- If the query is short or ungrammatical, still return the remaining content entity.

Examples:
Query: why fatigue caused?
Output: ["fatigue"]

Query: Why does lack of sleep cause fatigue?
Output: ["lack of sleep", "fatigue"]

Query: 높은 온도는 왜 얼음을 녹이나요?
Output: ["high temperature", "ice melting"]

Query: What does software deployment depend on?
Output: ["software deployment"]
"""

    user_prompt = f"Query: {query}"

    response = ollama.chat(

        model=config['llm_id'],

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        options={
            "temperature": 0
        }
    )

    result = response[
        "message"
    ]["content"]

    entities = parse_entity_response(result) 

    if entities:
        return entities

    fallback_entities = fallback_extract_entities(query)  
    print("[entity extraction fallback]", fallback_entities, flush=True)
    return fallback_entities

def print_retrieved_graph(results):
    graph_paths = refine_path_for_llm(results)

    print("\n[RETRIEVED GRAPH]", flush=True)

    if not graph_paths:
        print("No graph paths found.", flush=True)
        return

    for idx, path in enumerate(graph_paths, start=1):
        print(f"{idx}. {path}", flush=True) 

def retrieve_logical_paths(
    entities,
    max_hop=3
):  
    """
    엔티티 매칭 방식: 
    - exact cypyer(완전 매칭): 지정한 속성 값이 db에 저장된 값과 100% 일치할 떄만 값을 반환  
    -  fuzzy cypher(근사 매칭): 문자열의 유사성, 범위, 혹은 패턴을 기반으로 정확히 일치하지 않아도 비슷한 결과를 찾아냄
    - Neo4j에서 Levenshtein 거리를 이용한 유사도 검색 가능 
    """ 

    entities = [
        entity.strip()
        for entity in entities
        if isinstance(entity, str) and entity.strip()
    ]

    print("\n[INPUT ENTITIES]", flush=True)
    print(entities, flush=True)

    # exact matching
    exact_cypher = f"""
    MATCH path = (a)-[:CAUSE_OF|DEPENDS_ON|IS_A*1..{max_hop}]-(b)
    WHERE 
        any(name IN $entities WHERE toLower(a.name) = toLower(name))
        OR 
        any(name IN $entities WHERE toLower(b.name) = toLower(name))
    RETURN path
    LIMIT 20
    """

    # 근사 매칭 
    fuzzy_cypher = f"""
    MATCH path = (a)-[:CAUSE_OF|DEPENDS_ON|IS_A*1..{max_hop}]-(b)
    WHERE 
        any(name IN $entities WHERE toLower(a.name) CONTAINS toLower(name) OR toLower(name) CONTAINS toLower(a.name))
        OR 
        any(name IN $entities WHERE toLower(b.name) CONTAINS toLower(name) OR toLower(name) CONTAINS toLower(b.name))
    RETURN path
    LIMIT 20
    """

    print("\n[GENERATED CYPHER - EXACT MATCH]", flush=True)
    print(exact_cypher, flush=True) 

    try:

        with driver.session() as session:
            # 완전 매칭으로 그래프 먼저 검색 
            results = session.run(

                exact_cypher, 

                entities=entities
            )

            results = list(results) 

            # 검색된 그래프 결과가 있으면 바로 results 리턴 
            if results:
                print_retrieved_graph(results)
                return results

            print("\n[EXACT MATCH RESULT] No paths found. Trying fuzzy match...", flush=True)
            print("\n[GENERATED CYPHER - FUZZY MATCH]", flush=True)
            print(fuzzy_cypher, flush=True)

            # fallback: 완전 매칭으로 검색되는 결과가 없으면 fuzzy_cypher 쿼리 실행 
            results = session.run(

                fuzzy_cypher,

                entities=entities
            )

            results = list(results)
            print_retrieved_graph(results)
            return results    

    except Exception as e:

        print("\n[ERROR]")
        print(type(e))
        print(e)

        return []
    
# kg 검색 test 
# entities = ['감기', '원인']
# retrieve_logical_paths(entities)
