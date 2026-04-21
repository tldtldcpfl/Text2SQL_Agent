# Text2sql Agent
To build an effective Text-to-SQL agent that remains resilient to evolving table schemas, you need a system that decouples schema retrieval from query generation. A robust architecture typically relies on a "Retrieve-then-Generate" flow, utilizing vector embeddings to bridge the gap between natural language intent and dynamic database structures.

Here is an architectural breakdown for designing such an agent. 