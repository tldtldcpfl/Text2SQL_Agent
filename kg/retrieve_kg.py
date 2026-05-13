import ollama
from neo4j import GraphDatabase
from utils.parse import refine_path_for_llm 
import json 
with open('config.json', 'r') as f:
    config = json.load(f)

# driver  
driver = GraphDatabase.driver(
    # NEO4J_URI
    config['neo4j_url'],

    # user/pw 
    auth=(
        config['neo4j_user'],
        config['neo4j_password']
    )
) 

def extract_query_entities( 
    query 
):
    "llm extracts entities from user query" 

    prompt = f""" 
Extract only important entities from query.

Return JSON list only.

Query:
{query}
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
            "temperature": 0
        }
    )

    result = response[
        "message"
    ]["content"]

    try:

        import json

        return json.loads(result)

    except:

        return []


def retrieve_logical_paths(
    entities,
    max_hop=3
): 

    # print("RETRIEVE LOGICAL PATHS DEBUG")
    # print("===================================")

    # print("\n[INPUT ENTITIES]")
    # print(entities)

    # cypher 쿼리 
    cypher = f"""
    MATCH path = (a)-[:CAUSE_OF|DEPENDS_ON|IS_A*1..{max_hop}]-(b)
    WHERE 
        any(name IN $entities WHERE toLower(a.name) = toLower(name))
        OR 
        any(name IN $entities WHERE toLower(b.name) = toLower(name))
    RETURN path
    LIMIT 20
    """

    print("\n[GENERATED CYPHER]")
    print(cypher)

    paths = []

    try:

        with driver.session() as session:
            # cypher 쿼리 이후 검색된 record 객체: node와 path 객체를 포함 
            results = session.run(

                cypher,

                entities=entities
            )

            results = list(results)
            # print('[debug] cypher_results:\n', results)
            return results 
            
            # print("\n[RAW QUERY RESULT COUNT]")
            # print(len(results))

            # # -------------------------------------------------
            # # if no result retrieved

            # if len(results) == 0:

            #     print("\n[WARNING]")
            #     print(
            #         "No graph paths found."
            #     )

            #     # =============================================
            #     # check existing nodes
            #     # =============================================

            #     print("\n[CHECK EXISTING NODES]")

            #     # cypher graph query   
            #     for ent in entities:
                    
            #         check_query = """
            #         MATCH (n)

            #         WHERE toLower(n.name)
            #         CONTAINS toLower($ent)

            #         RETURN n.name
            #         LIMIT 10
            #         """ 
                
            #         node_result = session.run(

            #             check_query,

            #             ent=ent
            #         ) 

            #         matched = [
            #             r["n.name"]
            #             for r in node_result
            #         ]

            #         print(
            #             f"\nEntity: {ent}"
            #         )

            #         print(
            #             f"Matched Nodes: {matched}"
            #         )

            #     return [] 

    except Exception as e:

        print("\n[ERROR]")
        print(type(e))
        print(e)

        return []