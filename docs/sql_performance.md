# SQL Performance Comparison 

| Model | Latency | Accuracy |
|:---|:---|:---| 
| qwen2.5-7b(base) | a | a |
| basew/ filtered context | a | a |
| qwen2.5-7b-q4 | a | a | 
| q4 w/ filtered context | 2.65s | a | 

Note: quantization (q4) 

## Pipelines
load full schema → filter_schema → generate_sql → validate_sql → run_sql (db connection)   

