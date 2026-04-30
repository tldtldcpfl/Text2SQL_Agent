# Self-Reflexion of SQL Query Generation
SQL 생성에서 self-reflexion 루프가 효과적으로 동작하기 위해서는 단순히 정답/오답을 분류하는 것으로 끝날 것이 아니라, "틀리는 과정과 고치는 과정"에 대한 논리 로직을 임베딩 모델이 학습할 수 있어야한다. 
> **Reflexion Process 정의:** 문제 → 오답 생성 → 에러 인식 → 원인 분석 → 수정 계획 → 정답 도출
> 이를 위해, 훈련 데이터는 다음과 같이 구성되어야한다.

## Reflexion 궤적(Trajectory) 데이터셋 구성
- Syntax correcton: 
- Schema alignment:
- Logical refinement: 
