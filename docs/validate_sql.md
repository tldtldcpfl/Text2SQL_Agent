##  Validate SQL Query 

LLM이 생성한 sql 쿼리 검증은 크게 3가지 레벨에서 수행한다. 
- 구문 레벨: select, update, insert 구문 키워드 단위 필터링
- 논리 레벨: where 절의 조건문, join 절의 테이블 관계 등 논리적 오류 확인 
- 보안 레벨: 민감한 데이터 (ex. 테이블명, 컬럼명) 접근 제한 
<br>
<img width="786" height="363" alt="image" src="https://github.com/user-attachments/assets/e6bfc7dc-7fc4-4d90-95b7-c5543fe0806a" />

## Usage
유저의 자연어 질의 시 전체 테이블 스키마에서 유사도 검색 기반 관련도가 높은 테이블명, 컬럼명, 외래키명 추출한다. 이후, 데이터베이스에서 쿼리 실행 결과를 테이블 타입, 바 차트 타입, 자연어 타입으로 유저에게 출력한다. 

<br>
<img width="737" height="360" alt="image" src="https://github.com/user-attachments/assets/6d82a114-123e-45bc-86ca-e6c6feaac737" />

