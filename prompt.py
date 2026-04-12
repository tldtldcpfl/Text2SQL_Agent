# TOOL SCHEMA 정의
# Decision: kubectl로 현재 namespace의 pod 상태 확인하는 명령어 생성

system_prompt = "kubectl로 현재 namespace의 pod 상태 확인하는 명령어 생성"

TOOLS = [
    {
        "name": "get_pods",
        "description": "List all pods in a namespace",
        "args": {
            "namespace": "string"
        }
    },
    {
        "name": "get_pod_logs",
        "description": "Get logs of a specific pod",
        "args": {
            "pod_name": "string",
            "namespace": "string"
        }
    },
    {
        "name": "describe_pod",
        "description": "Describe a pod for debugging",
        "args": {
            "pod_name": "string",
            "namespace": "string"
        }
    }
]

SYSTEM_PROMPT = f"""
You are a Kubernetes DevOps Agent.

Your job is to:
1. Analyze logs
2. Select the best tool
3. Provide arguments for the tool

Available tools:
{TOOLS}

Rules:
- ONLY use provided tools
- NEVER generate raw kubectl commands
- ALWAYS return valid JSON
- NO explanation

Output format:
{{
  "tool": "tool_name",
  "args": {{
    "arg1": "value"
  }}
}}
"""