# DevOps Agent
An intelligent agent framework for automating Docker container builds, execution, and lifecycle management.

### Motivation
SRE engineers often face high pressure and sleep deprivation due to late-night incident responses. This framework was born to alleviate the stress and burden of 2 AM manual interventions. By automating Docker build and execution workflows, we aim to give engineers their nights back and ensure a more resilient system. That's why I built this framework—to turn stressful midnight fixes into seamless, automated workflows.


### K8S Tool Calling 
The agent interacts with the Kubernetes cluster through a set of predefined tools. These tools wrap the Kubernetes Python client API and provide safe, structured access to cluster resources.

The agent does not generate or execute raw kubectl commands. Instead, it communicates with the Kubernetes cluster via a Python server using the official Kubernetes API. By utilizing the Kubernetes Python client (e.g., `list_namespaced_pod`), it performs pod retrieval and operational tasks in a safe, structured, and programmatic way.