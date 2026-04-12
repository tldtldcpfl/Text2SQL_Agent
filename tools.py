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
from kubernetes import client, config
config.load_kube_config()
