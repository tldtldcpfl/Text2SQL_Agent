## Qwen-Embedding for semantic search
Qwen 임베딩 모델은 qwen 파운데이션 모델을 기반으로 텍스트 입력을 벡터로 생성하기위해 듀얼 인코더 방식을 채택한다.  

<br>
 
## Qwen2.5-7b decoder-only for generation
이  모델이 스키마 기반 sql 생성 task에 적합한 이유는 다음과 같다. 
- 스키마 적응력: 테이블 구조 컬렴명, 데이터 타입 등 sql 생성에 필요한 '스키마 정보'를 프롬프트로 입력했을 때, 모델이 이를 이해하고 쿼리 구조에 반영하는 능력이 강력하다.
- 사전 핛습 시 코딩 및 논리 추론 task에 특화된 점: sql은 일반 자연어보다 구조적 '코드'에 가깝다. 이에 따라, qwendms join, sub 쿼리 등 sql 문법을 준수하여 쿼리를 생성하는 능력이 우세하다.

<br>

### 유저 쿼리와 스키마 간 논리적 매핑 능력 비교
> qwen2.5-7b (decoder only) **vs.** all-minilm (encoder only)
- 두 모델의 {유저 쿼리, 스키마} pair 간 논리적 매핑 능력을 기준으로 성능을 비교한다. 
- All-MiniLM-L6-v2 임베딩 모델은 Sentence-BERT 계열의 임베딩 모델(encoder only)로 각 토큰의 문맥적 의미가 반영된 벡터를 추출한 후, mean pooling을 통해 평균내어 문장 전체를 대표하는 하나의 고차원 벡터로 변환한다. 
