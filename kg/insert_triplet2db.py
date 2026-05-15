from neo4j import GraphDatabase
import json 
from pathlib import Path
from tqdm import tqdm 

# config 
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.json"

with open (CONFIG_PATH, 'r') as f:
    config = json.load(f)

# driver: python app이 neo4j db와 연결
driver = GraphDatabase.driver(
    # NEO4J_URI
    config['neo4j_url'],

    # user/pw 
    auth=(
        config['neo4j_user'],
        config['neo4j_password']
    )
)

# normalzie relation name 
def neo4j_relation(rel):
    """대문자 타입만 지원"""
    return rel.upper()
 
def create_entity_node(
    tx,

    entity_name
):
    """entity node 생성"""

    query = """
    MERGE (e:Entity {name: $name})
    """

    tx.run(

        query,

        name=entity_name
    )

def create_relation(

    tx,

    head,

    relation,

    tail
):
    """"
    관계 엣지 생성 방식:
    - MERGE 문을 통해 Upsert(Update + Insert) 수행 
    - 노드 생성: 엔티티 라벨을 가진 노드 중 {name} 속성이 $head와 일치하는 노드가 있는지 확인
    - 관계 edge 생성/연결: 각 노드는 자신과 연결된 관계들의 리스트를 보유
    - structural link: merge는 head 노드와 tail 노드 사이에 relation 엣지를 연결 
    """ 

    relation = neo4j_relation(
        relation
    )

    # Graph DB insert 쿼리  
    query = f"""
    MERGE (h:Entity {{name: $head}})
    MERGE (t:Entity {{name: $tail}})
    MERGE (h)-[r:{relation}]->(t)
    """

    tx.run(

        query,

        head=head,

        tail=tail
    ) 

# insert llm-based triplets into neo4j
def insert_triplets_to_neo4j(

    triplets
):

    with driver.session() as session:

        for t in triplets:
            # triple 구성: head-relation-tail 
            head = t["head"]

            relation = t["relation"]

            tail = t["tail"]
            # label, node, 속성과 값 생성 
            session.execute_write(

                create_relation,

                head,

                relation,

                tail 
            )


def build_kg_from_dataset(

    eval_data,

    model_id
):
    """비정형 문서 데이터셋에서 엔티티 추출 이후 neo4j에 그래프 적재"""

    total_triplets = 0

    for sample in tqdm(
        eval_data,
        desc="Building KG from extracted triplets"
    ):

        # -------------------------------------------------
        # document
        # -------------------------------------------------

        document = sample[
            "document"
        ]

        # -------------------------------------------------
        # llm extraction
        # -------------------------------------------------
        from kg.extraction import llm_extract_triplet 
        llm_triplets = llm_extract_triplet(

            model_id=model_id,

            document_input=document
        )

        # -------------------------------------------------
        # normalization
        # -------------------------------------------------
        from kg.utils.parse import normalize_triplets
        llm_triplets = normalize_triplets(
            llm_triplets
        )

        # -------------------------------------------------
        # insert into neo4j
        # -------------------------------------------------

        insert_triplets_to_neo4j(
            llm_triplets
        )

        total_triplets += len(
            llm_triplets
        )

    print("\n================================")
    print("KG BUILD COMPLETE")
    print("================================")

    print(
        f"Inserted Triplets: {total_triplets}"
    )  

# json 데이터 경로
# with open(config['eval_data_path'], 'r', encoding='utf-8') as f:
#     json_data = json.load(f) 
# build_kg_from_dataset(json_data, config['llm_id'])  
