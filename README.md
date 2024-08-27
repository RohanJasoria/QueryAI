# QueryAI

**QueryAI** is a Python-based project designed to provide accurate, context-aware answers to user queries. By leveraging the power of the **SentenceTransformer** library, QueryAI efficiently stores summary documents as vectors in an Elasticsearch database. It exposes a **RESTful API** that allows users to ask questions related to the stored context.

When a user submits a query, QueryAI retrieves the most relevant information using KNN search i.e. K nearest neighbours. The retrieved answers are then refined accordong to the asked question and converted into a human-readable format using the T5 model which is provided by the Hugging Face Transformers library, ensuring that the response is both accurate and easy to understand.

## RESTful API

### Endpoints

- **`/ask`**:
  - **Input**: Accepts a user query along with a `queryId`.
  - **Functionality**:
    - Searches for the top results with a cosine similarity score greater than 0.7.
    - Combines and refines the search results according to asked question to generate a high-quality response.
    - Synchronizes the `Answer` collection in MongoDB, storing the generated response against the `queryId`.
    - Indexes the query with `queryId` for future retrieval of similar questions.
  - **Output**: Returns the refined response to the user query.

- **`/deleteAllRecords`**:
  - **Input**: None
  - **Functionality**: Clears all data from the Elasticsearch database, removing records across all indexes.
  - **Output**: Returns a status indicating whether the operation was successful.

- **`/indexData`**:
  - **Input**: A paragraph of generic content.
  - **Functionality**: 
    - Breaks the paragraph into individual sentences.
    - Stores the sentence embeddings in the vector database under a generic index.
  - **Output**: Returns a status indicating whether the operation was successful.

- **`/indexContent`**:
  - **Input**: A paragraph of content associated with a specific index.
  - **Functionality**: 
    - Breaks the paragraph into individual sentences.
    - Stores the sentence embeddings in the vector database under the specified index.
  - **Output**: Returns a status indicating whether the operation was successful.

- **`/getRelatedQueryIds`**:
  - **Input**: A user query.
  - **Functionality**: 
    - Searches the query index for top results with a cosine similarity score greater than 0.9.
  - **Output**: Returns a list of `queryId`s that are similar to the provided query.

## Key Features
- **Contextual Data Indexing**: Supports storing paragraphs as vector embeddings, either under a generic or specific index, enabling efficient context retrieval.
- **Dynamic Query Matching**: Provides robust semantic search capabilities using SentenceTransformer, allowing high-precision matching of user queries with stored content.
- **Contextual Query Insights**: Retrieves related `queryId`s based on cosine similarity, enhancing the system’s understanding of similar queries.
- **Scalable Data Management**: Includes endpoints for bulk data management, such as clearing all records in the Elasticsearch database, ensuring flexible and scalable operations.
- **Human-Readable Responses**: Utilizes GenAI to refine and enhance the quality of responses, making them accurate and easy to understand.
- **RESTful API**: Exposes a straightforward and comprehensive API, facilitating easy integration of QueryAI into various applications and services.

## Use Cases
- **Knowledge Management Systems**: Efficiently store and retrieve contextual information, improving the accuracy and accessibility of knowledge bases.
- **Customer Support Automation**: Automate responses to common customer queries with context-aware answers, enhancing customer satisfaction.
- **Educational Platforms**: Provide students with precise, context-driven answers, improving learning outcomes.
- **Intelligent Content Indexing**: Index and manage large volumes of content, enabling fast and accurate retrieval of contextually relevant information.
- **Search and Recommendation Engines**: Power advanced search and recommendation systems by leveraging contextual understanding and semantic search.

## Technologies Used
- Python
- Elasticsearch
- SentenceTransformer
- Hugging Face Trasformer
- MongoDB
