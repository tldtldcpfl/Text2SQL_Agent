# main.py 
import requests 
import json 
from prompt import system_prompt 
from tools import get_pods, get_pod_logs, describe_pod, namespace, pod_name
from validator import perform_log_validation 

# ollama 엔드포인트: ollama는 로컬에서 실행되는 LLM 서버
OLLAMA_URL = "http://localhost:11434/api/generate"

def main():
    """
    Ollama (qweun2.5:3b) 모델에 system_prompt를 보내고, 응답을 받아서 JSON으로 파싱한 후,
    응답에 포함된 "tool" 필드에 따라 Kubernetes API 함수를 호출하는 방식
    """
    # LLM 서빙 엔드포인트 호출 
    response = requests.post(
        OLLAMA_URL,
        # json 형식으로 리턴 받기 위해 json 파라미터 사용
        json={
            "model": "qwen2.5:3b",
            "prompt": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        }
    )
    response = response.json()['response']
    result = json.loads(response)

    # 함수명 조건 
    if "get_pods" in result["tool"]:
        print("[info] get pods 함수 실행")
        # get_pods() 함수 실행
        tool_call_result = get_pods(namespace)
 
        # get_pods 호출 후 자동으로 로그 검증 수행 
        print("[info] perform_log_validation 함수 실행")
        log_validation_result = perform_log_validation(pod_name, namespace, get_pod_logs)
        print(f"[log validation result] {log_validation_result}") 
   
    # LLM의 결과에 따라 로그 검증 함수를 조건부로 호출  
    # elif "validate_logs" in result["tool"]:
    #     print("[info] validate_logs 함수 실행")
    #     val_result = perform_log_validation() 
    #     print(f"[log validation result] {val_result}") 
        
    #print(tool_call_result.items)
    return tool_call_result.items if "get_pods" in result["tool"] else None

if __name__ == "__main__":
    main()  