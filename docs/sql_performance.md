# SQL Performance Comparison 

| Model | Latency | Accuracy |
|:---|:---|:---| 
| qwen2.5-7b(base) | a | a |
| basew/ filtered context | a | a |
| qwen2.5-7b-q4 | a | a | 
| q4 w/ filtered context | 2.65s | a | 

Note: quantization (q4) 

## Pipelines
load full schema → filter_schema → generate_sql → validate_sql → run_sql (db connection)   
<br>

## Evaluation Benchmarks 
LLM이 자연어 질문을 SQL 쿼리로 얼마나 정확하게 변환하는지 평가 시 활용할 수 있는 Text-to-SQL 표준 벤티마크는 다음과 같다. 
- Spider Test@M-Schema
- Spider Test@DDL
- BIRD Dev@M-Schema
- BIRD Dev@DDL
  
## 평가 요소 및 지표 
- **Schema Linking (스키마 링킹):** 유저 질문에 등장하는 엔티티가 데이터베이스의 어떤 테이블/컬럼과 매핑되는지 식별한다.
- **Schema Encoding (스키마 인코딩):** 테이블 간의 연관성과 컬럼 간 관계를 모델이 이해하도록 구조화한 것이다.
- **Execution Accuracy (실행 정확도):** 생성된 SQL 쿼리를 실제 DB에서 실행했을 때, 저앋ㅂ 쿼리의 실행 결과와 동일한 비율
- **Exact Match (일치 정확도):** SQL 쿼리 구문 자체가 정답과 일치하는지 평가 
