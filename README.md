# K8s Agent
An intelligent agent framework for automating Docker container builds, execution, and lifecycle management.

### Motivation 
SRE(Site Reliability Engineering) engineers often face high pressure and sleep deprivation due to late-night incident responses. This framework was born to alleviate the stress and burden of 2 AM manual interventions. By automating Docker build and execution workflows, we aim to give engineers their nights back and ensure a more resilient system. That's why I built this framework—to turn stressful midnight fixes into seamless, automated workflows.


### K8S Tool Calling 
The agent interacts with the Kubernetes cluster through a set of predefined tools. These tools wrap the Kubernetes Python client API and provide safe, structured access to cluster resources.

The agent does not generate or execute raw kubectl commands. Instead, it communicates with the Kubernetes cluster via a Python server using the official Kubernetes API. By interacting with Kubernetes API objects via HTTP, it performs container management and operational tasks. 

### Components
This project consists of several key components that work together to benchmark and compare log anomaly detection approaches in Kubernetes environments.

#### Analyzer
The analyzer module is the core component responsible for processing Kubernetes cluster logs and detecting anomalies. It implements two primary approaches:

- LLM Prompt-Based Detection: Uses a Large Language Model (LLM) with a specialized Kubernetes/SRE expert prompt to classify logs as normal (0) or anomalous (1).
- Alternative Detection Method: A comparative approach (e.g., rule-based or machine learning-based) for benchmarking effectiveness against the LLM method.

#### Tool
The tool.py module provides utility functions and scripts for data preprocessing, log ingestion, and integration with Kubernetes APIs. It handles tasks such as log parsing, filtering, and preparing datasets for analysis.

#### Prompt
The prompt module manages the LLM prompts used in the anomaly detection process. It includes predefined templates for expert-level classification, such as the example prompt that instructs the LLM to return only a binary classification (0 or 1) for each log entry.

#### Validator
The validator module is responsible for validating the results of anomaly detection. It includes functions for accuracy assessment, false positive/negative analysis, and performance metrics comparison between the two analyzer approaches, ensuring reliable benchmarking.
