# Safety Guardrails
> **Why this matters?**

가드레일 에이전트는 모델의 입/출력을 도메인 정책(위험 분류 체계)에 맞게 제어하기 위해 동작하는 main agent (Text-to-SQL)의 sub agent이다. 본 프로젝트에서는 규칙 기반 가드레일과 소형 임베딩 모델 기반 가드레일로 하이브리드 방식을 채택한다. 
Master/sub agent 간 context 분리 및 사용 시나리오별 tool/data 접근 권한을 제어하기 위한 기능이다. 이를 통해, 테아블 조회/검색/쿼리 생성/ 쿼리 실행 프로세스의 각 단계의 불필요한 데이터 접근을 방지할 수 있다. 궁극적으로, 프로덕션 환경에서 에이전트가 발생시킬 수 있는 보안 위협을 사전에 방지할 수 있다.   
<br>

## Agent Trajectory Safety Evaluation
에이전트 궤적 수준 안전 평가는 에이전트가 복합적인 task를 수행하는 과정에서 발생하는 전체 행동 흐름(trajectory)이 안전한지, 위험 요소가 없는지 평가하는 방법이다. 멀티 턴 대화에서 대화 문맥이 길어지고 여러 도구가 연동되는 환경에서 위험 요소를 탐지하는 건 매우 중요하다. 

여러 step을 거치는 동안 발생하는 여러 도구 사용, api 호출 로그 추적/분석을 통해 위험 요소를 탐지한다. [agent trajectories 평가 데이터셋](https://huggingface.co/datasets/AI45Research/ATBench)에 대해 핵심 평가 항목은 다음과 같다.
- 위험 출처 (risk source): 유해한 쿼리, **부적절한 tool name** 사용
- domain-level과 tool_name-level 분류 정확도 

<br>

## ATBench Baseline 측정
자연어 질문과 타겟 SQL 쿼리, 그리고 해당 데이터베이스 스키마로 구성된다. all-minilm 베이스 모델의 retriever 성능을 측정을 위해 사용 가능한 지표는 아래와 같다.
- **recall@k:** 검색된 상위 k개의 테이블 리스트에 실제 정답 sql에 사용된 테이블이 포함되어 있는지를 측정한다.  
- **hit rate@k:** 상위 k개의 추출된 테이블 중, 실제 정답 sql에 포함된 테이블이 적어도 하나 이상 존재하는 질문의 비율 
- **mrr:** 정답 테이블이 검색 결과의 몇 번째 순위에 위치하는지를 측정 
