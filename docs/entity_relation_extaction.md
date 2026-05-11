# Entity Relation Extraction 

| **model** | **precision** | **recall** | **f1** | **directional_accuracy** | **reverse_direction_errors** | **avg_latency_sec** | **correlated_with_f1** | **cause_of_f1** | **depends_on_f1** | **is_a_f1** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Encoder (GLiNER) | 0.0698 | 0.9767 | 0.1302 | 0.1293 | 6 | 0.1818 | 0.2667 | 0.1005 | 0.1606 | 0.0940 |
| LLM | 0.7321 | 0.9535 | 0.8283 | 0.8488 | 2 | 3.2467 | 0.9091 | 0.8696 | 0.7407 | 0.8462 |