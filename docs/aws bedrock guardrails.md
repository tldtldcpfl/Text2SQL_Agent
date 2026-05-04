
# AWS Bedrock Guardrails 
아마존 베드락에서는 가드레일 기능을 application 엔드포인트 호출 이전에 컨텐츠 필터링을 위해 통과시키는 컴포넌트로 제공한다. 

## How it works 
세부적으로, 가들드레일 기능을 통해 금지된 주제, 컨텐츠 필터, 민감 정보 필터, 단어 필터 등이 가능하다. 필터링 기준 카테고리는 사용 시나리오별 컨텐츠 정책(policy)에 따라 달라진다. 민감 정보 필터의 경우 PII 검열 삭제와 정규 표현을 통해 개인 정보를 식별하고 마스킹한다.  

## Reference
- https://pages.awscloud.com/rs/112-TZM-766/images/GAI213-English.pdf
