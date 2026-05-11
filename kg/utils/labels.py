# entity labels 사전 정의  
entity_labels = [
    "Concept",
    "Metric",
    "Tool",
    "Organization"
]

# 계층성 /인과성/ 멀티 홉 논리 구조 라벨
# challenge: llm이 cause of / denpends on 두 directional-relation 클래스를 자주 혼동함 (결정 경계선이 뭉툭한 부분)   
relation_labels = [
    "is_a",  # a is a category of b (계층 관계: b가 a의 상위 개념)
    "cause_of",  # a→b 
    "correlated_with", # covary without causality 
    "depends_on" # b→a 
]  

# 한국어 조사 정규 표현 처리  
KOREAN_PARTICLES = [
    "은", "는", "이", "가",
    "을", "를", "의", "에",
    "와", "과", "로", "으로"
]

RELATION_MAP = {
    "causes": "cause_of",
    "cause of": "cause_of",
    "related to": "correlated_with",
    "depends on": "depends_on",
    "is a": "is_a"
}