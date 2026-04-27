##  Validate SQL Query 

LLM이 생성한 sql 쿼리 검증은 크게 3가지 레벨에서 수행한다. 
- 구문 레벨: select, update, insert 구문 키워드 단위 필터링
- 논리 레벨: where 절의 조건문, join 절의 테이블 관계 등 논리적 오류 확인 
- 보안 레벨: 민감한 데이터 (ex. 테이블명, 컬럼명) 접근 제한  


