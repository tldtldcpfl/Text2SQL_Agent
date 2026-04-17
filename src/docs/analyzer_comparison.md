## Analyzer A/B Test: Kubernetes Log Anomaly Detection Benchmark

### Overview

Aanalyzer is a module responsible for detecting anomalies from Kubernetes cluster logs. 

This project compares two different approaches to identify the most effective architecture for production-grade log anomaly detection.

---

## Compared Approaches

### A. LLM Prompt-Based Log Anomaly Detection

This approach uses a Large Language Model with a Kubernetes / SRE expert system prompt to classify logs.

### Example Prompt

```text
You are a Kubernetes SRE expert.

Classify the following log:

0 = normal
1 = anomaly

Return only the number. 