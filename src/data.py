import warnings
warnings.filterwarnings('ignore')

from sentence_transformers import InputExample
from torch.utils.data import DataLoader

# 원본 데이터를 딕셔너리 리스트로 재정의 (JSON 구조와 동일)
raw_train_data = [
    # 1. 스키마 오류
    {
        "texts": [
            "Error: no such column: user_name", 
            "현재 참조하고 있는 컬럼이 스키마 정보와 일치하지 않습니다. 테이블 메타데이터를 확인하여 정확한 컬럼명으로 수정하세요."
        ],
        "label": 1.0
    },
    {
        "texts": [
            "Unknown column 'agee' in 'field list'",
            "존재하지 않는 컬럼을 참조했습니다. 컬럼명을 다시 확인하세요."
        ],
        "label": 1.0
    },

    # 2. GROUP BY 오류
    {
        "texts": [
            "column 'total_price' must appear in the GROUP BY clause",
            "집계 함수가 아닌 컬럼은 GROUP BY 절에 포함되어야 합니다."
        ],
        "label": 1.0
    },
    {
        "texts": [
            "SELECT list is not in GROUP BY clause and contains nonaggregated column",
            "집계되지 않은 컬럼이 GROUP BY 없이 사용되었습니다."
        ],
        "label": 1.0
    },

    # 3. 데이터 타입 오류
    {
        "texts": [
            "Invalid input syntax for integer: 'abc'",
            "정수형 컬럼에 문자열이 입력되었습니다. 데이터 타입을 확인하세요."
        ],
        "label": 1.0
    },
    {
        "texts": [
            "Cannot cast type text to integer",
            "데이터 타입 변환이 불가능합니다. 타입을 맞춰주세요."
        ],
        "label": 1.0
    },

    # 4. NULL 관련 오류
    {
        "texts": [
            "null value in column 'id' violates not-null constraint",
            "NOT NULL 제약 조건이 있는 컬럼에 NULL 값이 들어갔습니다."
        ],
        "label": 1.0
    },

    # 5. 테이블 존재하지 않음
    {
        "texts": [
            "relation 'userss' does not exist",
            "존재하지 않는 테이블을 참조했습니다. 테이블명을 확인하세요."
        ],
        "label": 1.0
    },

    # 6. JOIN 오류
    {
        "texts": [
            "column reference 'id' is ambiguous",
            "JOIN 시 동일한 컬럼명이 여러 테이블에 존재합니다. 테이블 alias를 명시하세요."
        ],
        "label": 1.0
    },

    # 7. 문법 오류
    {
        "texts": [
            "syntax error at or near 'FROM'",
            "SQL 문법 오류가 발생했습니다. 키워드 위치를 확인하세요."
        ],
        "label": 1.0
    },

    # 8. 함수 관련 오류
    {
        "texts": [
            "function sum(text) does not exist",
            "SUM 함수는 숫자 타입에만 사용할 수 있습니다."
        ],
        "label": 1.0
    },

    # 9. 권한 오류
    {
        "texts": [
            "permission denied for table users",
            "해당 테이블에 대한 접근 권한이 없습니다."
        ],
        "label": 1.0
    },

    # 10. division by zero
    {
        "texts": [
            "division by zero",
            "0으로 나눌 수 없습니다. 분모 값을 확인하세요."
        ],
        "label": 1.0
    }
]

# 2. TypeError 없이 InputExample 리스트 생성
# item이 딕셔너리이므로 item['texts'] 접근이 가능해집니다.
train_examples = [
    InputExample(texts=item['texts'], label=item.get('label', 1.0)) 
    for item in raw_train_data
]


# 3. DataLoader 설정
# batch_size는 MacBook Air 환경을 고려해 8~16 사이를 추천합니다.
train_dataloader = DataLoader(
    train_examples, 
    shuffle=True, 
    batch_size=8
)