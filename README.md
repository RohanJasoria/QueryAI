# QueryAI

**QueryAI** is an advanced Python-based project designed to provide accurate, context-aware answers to user queries. By leveraging the power of the **SentenceTransformer** library, QueryAI efficiently stores summary documents as vectors in an Elasticsearch database. It exposes a RESTful API that allows users to ask questions related to the stored context.

When a user submits a query, QueryAI retrieves the most relevant information using semantic search. The retrieved answer is then refined and converted into a human-readable format using the **GenAI** library, ensuring that the response is both accurate and easy to understand.

## Key Features
- **Contextual Understanding**: Stores documents as vectors to preserve context and provide more accurate answers.
- **Semantic Search**: Utilizes SentenceTransformer for high-quality semantic matching of user queries with stored content.
- **Human-Readable Responses**: Enhances retrieved answers using GenAI, making them clearer and more understandable.
- **RESTful API**: Easy-to-use API for integrating QueryAI into other applications or services.

## Use Cases
- Knowledge management systems
- Customer support automation
- Educational platforms with contextual search
- Any application requiring intelligent, context-aware responses

## Technologies Used
- Python
- Elasticsearch
- SentenceTransformer
- GenAI
