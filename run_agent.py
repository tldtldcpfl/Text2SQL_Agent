import requests
from propmt import system_prompt 
# ollama 엔드포인트 구성 설명 - ollama는 로컬에서 실행되는 LLM 서버입니다.

OLLAMA_URL = "http://localhost:11434/api/generate"

def main():
    res = requests.post(
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
    return res.json()["response"]

    
if __name__ == "__main__":
    main()  