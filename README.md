# Text2SQL Agent
add overview desc and architecture img

## Why This Matters
In enterprise environments with thousands of RDBMS tables and complex, evolving schemas, the challenge is not just "writing SQL,but maintaining enterprise-grade data integrity and performance".  

## Problem Definition 
LLM ignores table schema
LLMs can generate SQL queries by directly injecting table schema information (e.g., table names and columns) into the system prompt. A common approach is to provide the schema as context and rely on system prompt. 

However, this naive approach introduces several critical limitations:
- Ignoring key columns: LLM often fail to indentify and utilize the most relavant columns for a given query. Instead, they may select semantically similar but incorrect columns.  

- Incorrect or Missing JOIN conditions

- Incomplete WHERE clauses 

- Performance degradtion 

### Root Cause 
These issues stem from a fundamental limitation of LLM: non-deterministic 

## Approach: Schema Validation Agent 
To address these limitations, we introduce a Schema Validation Agent framework. Instread of relying solely on prompt-based SQL generation: Validate and refine SQL queries using **schema-aware structural checks**. 

**Usage Strategy:**
Fundamentally, this approach allows for precise SQL generation control by the agent, along with table and column-level access management.
