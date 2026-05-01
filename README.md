# Schema-Aware RAG for Text2SQL
The core logic of this agent revolves around a Dynamic Schema Selection strategy rather than feeding the entire database schema into the LLM. This ensures token efficiency and minimizes sql hallucinations.

## Vector-Based Schema RetrievalEncoder 
Utilizing all-MiniLM-L6-v2 (or the fine-tuned paraphrase-multilingual model) to index all table names and column descriptions.Similarity Search: When a user query is received, the agent performs a semantic search to retrieve only the top-$k$ most relevant table and column metadata.Selective Injection: Only the retrieved metadata is injected into the prompt, providing the LLM with a focused "contextual schema" relevant to the specific question.

## Multi-Agent Pipeline with Reflexion
Generation Agent: Constructs the SQL query using the pruned schema.

Validation Agent: Executes the query and captures any database engine feedback.

## Reflexion Agent 
If the execution fails, this agent uses the fine-tuned embedding model to find a matching correction guide for the specific error (e.g., column ambiguity or syntax mismatch).
<br>

## Why This Strategy? 
Cost Efficiency: By reducing the prompt size, we significantly lower the inference cost for long-running agentic workflows.

Scalability: This approach allows the agent to handle databases with hundreds of tables, where feeding the full schema would be technically impossible.

Precision: LLMs perform better when given a "narrow and deep" context rather than a "broad and shallow" one.
