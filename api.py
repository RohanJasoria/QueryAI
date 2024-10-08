# api.py

from fastapi import FastAPI
from pydantic import BaseModel
from elasticsearch_client import ElasticsearchClient
from embedding import EmbeddingGenerator
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import pandas as pd
from io import BytesIO
from pydantic import BaseModel
from fastapi import HTTPException
from answer import AutoGeneratedResponse
import time
from mongo_client import collection


class Paragraph(BaseModel):
    text: str


# Define a Pydantic model for the input data
class Query(BaseModel):
    question: str
    queryId: str

class QueryStatement(BaseModel):
    question: str

class IndexContext(BaseModel):
    context: str
    index: str

# Create FastAPI app
app = FastAPI()

# Instantiate the Elasticsearch client, embedding generator and nlp model
es_client = ElasticsearchClient()
embedding_generator = EmbeddingGenerator()
tokenizer = AutoTokenizer.from_pretrained("t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
nlp = pipeline("summarization", model=model, tokenizer=tokenizer)

# Define lifespan function
async def lifespan(app: FastAPI):
    # Startup logic
    es_client.create_index()
    yield
    # Shutdown logic
    pass

# Create FastAPI app
app = FastAPI(lifespan=lifespan)



@app.post("/ask")
async def ask_question(query: Query):
    # Generate the embedding for the question
    query_embedding = embedding_generator.generate_embedding(query.question)
    print("Request coming in")

    # Search for similar documents
    similar_documents = es_client.search_similar(query_embedding)

    # Top Results
    top_results = [hit["_source"]["text"] for hit in similar_documents]
    combined_context = " ".join(top_results)
    if len(combined_context.strip()) < 5:
        return {"response": ""}

    #Refine Response
    refined_response = nlp(combined_context, max_length=500, min_length=5, do_sample=False)

    #Generating Answer
    aiResponse = AutoGeneratedResponse(
        queryId = query.queryId,
        answer = refined_response[0].get('summary_text'),
        aiGenerated = True,
        userId = "0",
        deleted = False,
        supportVerified = False,
        upvotes = 0,
        timestamp = int(time.time() * 1000)
    )

    #Inserting AI Response in MongoDB
    collection.insert_one(aiResponse.model_dump())
    print("Data inserted in DB succesfully")

    #Indexing Query in ES
    es_client.index_query(query.question, query.queryId, query_embedding)
    print("Query inserted in ES succesfully")

    return {"response": refined_response}



@app.get("/deleteAllRecords")
def delete_all_records():
    es_client.delete_records()
    return {"message": "Vector DB Cleanes Successfully"}



@app.post("/indexData")
async def index_data(paragraph: Paragraph):
    # Split the paragraph into sentences by full stops
    sentences = [sentence.strip() for sentence in paragraph.text.split('.') if sentence.strip()]

    # Create a DataFrame with the sentences
    df = pd.DataFrame(sentences, columns=["context"])

    # Save the DataFrame to an in-memory Excel file
    excel_stream = BytesIO()
    df.to_excel(excel_stream, index=False)
    excel_stream.seek(0)

    # Index each sentence in Elasticsearch
    for sentence in sentences:
        embedding = embedding_generator.generate_embedding(sentence)
        es_client.index_document(sentence, embedding)

    return {"message": "Paragraph processed and indexed successfully"}


@app.post("/indexContent")
async def index_data(content : IndexContext):
    if not isinstance(content.context, str):
        raise HTTPException(status_code=400, detail="The context should be a string.")
    
    # Split the paragraph into sentences by full stops
    sentences = [sentence.strip() for sentence in content.context.split('.') if sentence.strip()]

    # Create a DataFrame with the sentences
    df = pd.DataFrame(sentences, columns=["contextInfo"])

    # Save the DataFrame to an in-memory Excel file
    excel_stream = BytesIO()
    df.to_excel(excel_stream, index=False)
    excel_stream.seek(0)

    # Index each sentence in Elasticsearch
    for sentence in sentences:
        embedding = embedding_generator.generate_embedding(sentence)
        es_client.index_document_given_index(sentence, content.index, embedding)

    return {"message": "Content processed and indexed successfully"}

@app.post("/getRelatedQueryIds")
async def get_related_query_ids(query: QueryStatement) :
    if not isinstance(query.question, str):
        raise HTTPException(status_code=400, detail="The context should be a string.")
    
    # Generate the embedding for the question
    query_embedding = embedding_generator.generate_embedding(query.question)

    # Search for similar documents
    similar_queries = es_client.search_similar_queries(query_embedding)

    # Get Ids
    ids = [item["_id"] for item in similar_queries]

    return {"response": ids}

