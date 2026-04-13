# 쿠버네티스 api 호출 및 실행 
# action: 실제 Kubernetes에 요청 보내는 함수들 
# 외부 kubernetes API 엔드포인트와 상호 작용

from kubernetes import client, config 

# kubernetes 초기화 
def k8s_init():
    config.laod_kube_config()
    # client
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces()

    # Namespace는 Pod, Service 등 리소스를 논리적으로 분리하는 가상 공간
    unique_namespaces = set()
    # Pod Name은 개별 컨테이너 묶음(Pod)의 고유 식별자
    unique_pod_names = set()
    for pod in pods.items:
        unique_namespaces.add(pod.metadata.namespace)
        unique_pod_names.add(pod.metadata.name)
    namespace = list(unique_namespaces)[0] if unique_namespaces else None
    pod_name = list(unique_pod_name)[0] 
    return namespace, pod_name

namespace, pod_name = k8s_init()

# function list 
def get_pods(namespace):
    return v1.list_namespaced_pod(namespace)

def get_pod_logs(pod_name, namespace):
    return v1.read_namespaced_pod_log(pod_name, namespace)

def describe_pod(pod_name, namespace):
    return v1.read_namespaced_pod(pod_name, namespace)