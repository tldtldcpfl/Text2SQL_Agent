# Schema Embedding Analysis

## Qwen2.5-7b Prompt Only


## Encoder: all-minilm 
all-minilm 인코더는 sentence-bert 기반의 384d 임베딩을 생성하는 경량화된 모델이다. 10억개의 query-docuemnt pair에 학습되어 문장의 general한 의미를 벡터화시키는데 최적화되어있다. 

하지만, 테이블 스키마(table_docs)와 같은 '구조화된 정보'는 일반 문장과 분포가 다르다. 즉, 동일한 임베딩 공간에서 자연어 문장 임베딩 분포와 json 스키마 임베딩 분포가 다르기 때문에, 코사인 거리 계산이 왜곡될 수 있다. 

## Distribution Shift 측정 
> P(natural language) ≠ P(schema)
Distribution(NL ↔ SQL) > Distribution(NL ↔ NL) measured by Jensen-Shannon Divergence(JSD)   
- JSD: 두 확률 분포 간 유사성 또는 차이를 측정하는 척도  
