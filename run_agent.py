# main.py 
import requests 
import json 
from prompt import system_prompt 
from tools import get_pods, get_pod_logs, describe_pod, namespace, pod_name

# ollama 엔드포인트 구성 설명 - ollama는 로컬에서 실행되는 LLM 서버입니다.
OLLAMA_URL = "http://localhost:11434/api/generate"

def main():
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
    #print(result, type(result))
    #return result

    # 함수명 조건 
    if "get_pods" in result["tool"]:
        print("[info] get pods 함수 실행")
        # get_pods() 함수 실행
        tool_call_result = get_pods(namespace)
        
    print(tool_call_result.items)
    return tool_call_result.items

if __name__ == "__main__":
    main()  