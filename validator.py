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

def perform_log_validation(pod_name, namespace, get_pod_logs):
    """로그 검증을 수행하는 함수 (매개변수로 의존성 주입)"""
    logs = get_pod_logs(pod_name, namespace)
    # print(f"[logs for validation] {logs}")  # 검증할 로그 출력
    result = validate_logs(logs) 
    return result

# test: perform_log_validation 함수 실행 
# valid_result = perform_log_validation(pod_name, namespace, get_pod_logs)
# print(valid_result)