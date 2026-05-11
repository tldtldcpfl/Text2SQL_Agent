def build_prompt(document_input):

    system_prompt = f"""
당신은 Knowledge Graph Triplet Extraction Engine 입니다.

주어진 문서를 분석하여,
반드시 아래 스키마에 정의된 Entity 및 Relation만 사용해
지식 그래프 triplet을 추출하세요.

[Ontology Schema]

Entity Types:
- Concept
- Metric
- Tool
- Organization

Allowed Relations:

1. is_a
- 계층/분류 관계
- 예:
  "BERT is_a Language Model"

2. cause_of
- 원인 -> 결과 방향만 허용
- 예:
  "Semantic Noise cause_of Retrieval Failure"

3. correlated_with
- 상관 관계
- 방향성 없음
- 대칭 관계

4. depends_on
- 의존 관계
- A depends_on B 의미:
  A는 B에 의존한다.
  B 변화가 A에 영향을 준다.

[Direction Constraints]

cause_of:
A -> B

depends_on:
A depends_on B
(B influences A)

절대 방향을 반대로 생성하지 마세요.

[Extraction Rules]

- 반드시 문서에 근거한 관계만 추출하세요.
- hallucination 금지.
- relation 이름은 반드시 아래 4개만 사용:
  ["is_a", "cause_of", "correlated_with", "depends_on"]

- 동일 의미 중복 triplet 금지.
- head/tail은 가능한 원문 유지.
- 관계가 애매하면 추출하지 마세요.
- JSON 외 텍스트 출력 금지.
- 반드시 JSON LIST 형식만 출력하세요.

[Output Format]

[
  {{
    "head": "...",
    "relation": "...",
    "tail": "..."
  }}
]

[Examples]

Input:
"Dense Retriever는 인과 방향성을 인코딩하지 못해 Semantic Noise를 발생시킨다."

Output:
[
  {{
    "head": "Dense Retriever",
    "relation": "cause_of",
    "tail": "Semantic Noise"
  }}
]

Input:
"Plant growth depends on sunlight."

Output:
[
  {{
    "head": "Plant growth",
    "relation": "depends_on",
    "tail": "sunlight"
  }}
]

[Document]
{document_input}
"""

    return system_prompt 