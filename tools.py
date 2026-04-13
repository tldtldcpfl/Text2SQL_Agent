# 쿠버네티스 실행 

# tools_list = [
#     {
#         "name": "kubectl_get_pods",
#         "description": "Get pod list",
#         "args": {
#             "namespace": "string"
#         }
#     },
#     {
#         "name": "kubectl_logs",
#         "description": "Get pod logs",
#         "args": {
#             "pod_name": "string"
#         }
#     }
# ]

# action: 실제 Kubernetes에 요청 보내는 함수들 
# 외부 kubernetes API 엔드포인트와 상호 작용
from kubernetes import client, config 

config.load_kube_config()
v1 = client.CoreV1Api() 

def get_pods(namespace):
    return v1.list_namespaced_pod(namespace)

def get_pod_logs(pod_name, namespace):
    return v1.read_namespaced_pod_log(pod_name, namespace)

def describe_pod(pod_name, namespace):
    return v1.read_namespaced_pod(pod_name, namespace)