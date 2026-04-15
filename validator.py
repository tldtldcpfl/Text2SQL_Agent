#  로그 데이터 필드 검증 
from tools import pod_name, namespace, get_pod_logs

ERROR_KEYWORDS = [
    "error", "exception", "failed",
    "panic", "oom", "crash", "timeout"
]

CRITICAL_K8S = [
    "CrashLoopBackOff",
    "OOMKilled",
    "ImagePullBackOff"
]


def validate_logs(log_text: str):
    log_text_lower = log_text.lower()

    # 1. level 기반
    if "level=error" in log_text_lower or "level=fatal" in log_text_lower:
        return True, "error level detected"

    # 2. k8s 상태
    for keyword in CRITICAL_K8S:
        if keyword.lower() in log_text_lower:
            return True, f"k8s critical: {keyword}"

    # 3. 일반 에러 키워드
    for keyword in ERROR_KEYWORDS:
        if keyword in log_text_lower:
            return True, f"error keyword: {keyword}"
        
    # If nothing goes wrong 
    return False, "normal"

# test: 로그 필드 검증 함수 실행
# logs = get_pod_logs(pod_name, namespace)
# # print(logs)  
# result = validate_logs(logs)
# print(result) 
