# tools list 정의 
tools_list = [
    {
        "name": "generate_sql",
        "description": "사용자의 자연어 질문을 입력받아 SQL 쿼리를 생성하는 함수입니다. 입력된 질문에 대해 데이터베이스 스키마 정보를 활용하여 최적화된 SQL 쿼리를 생성합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_query": {
                    "type": "string",
                    "description": "사용자의 자연어 질문입니다.",
                },
                "llm_id": {
                    "type": "string",
                    "description": "사용할 LLM 모델의 ID입니다.",
                },
                "system_prompt": {
                    "type": "string",
                    "description": "LLM에게 제공할 시스템 프롬프트입니다.",
                },
            },
            "required": ["user_query", "llm_id", "system_prompt"],
        }, 
    }
]
# print('[info] tools list:\n', tools_list)