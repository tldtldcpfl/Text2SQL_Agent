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
    
    """
    # LLM 서빙 엔드포인트 호출 
    
    

if __name__ == "__main__":
    main()  