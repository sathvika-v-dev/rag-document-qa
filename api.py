from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import UploadFile,File
import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import  PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
import shutil
from groq import Groq
import sqlite3
load_dotenv()
groq_client=Groq(api_key=os.getenv("GROQ_API_KEY"))
app=FastAPI()
embedding_model=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vector_store=Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)
class QuestionRequest(BaseModel):
    question:str
@app.get("/")
def home():
    return{"message":"RAG API is running!"}

@app.post("/upload")
def upload_pdf(file:UploadFile = File(...)):
    global vector_store
    file_path=f"uploaded_{file.filename}"
    with open(file_path,"wb")as buffer:
        shutil.copyfileobj(file.file,buffer)

    loader=PyPDFLoader(file_path)    
    documents=loader.load()
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks=text_splitter.split_documents(documents)
    vector_store=Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="chroma_db"
    )
    return {"message":f"{file.filename} uploaded and processed successfully!","chunks_created":len(chunks)}

@app.post("/ask")
def askquestion(request:QuestionRequest):
    query=request.question    

    results=vector_store.similarity_search(query,k=2)
    context="\n\n".join([doc.page_content for doc in results])
    response=groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role":"system","content":"you are a helpful assistant that answers questions based only on the provided context"},
            {"role":"user","content":f"context:\n{context}\n\nQuestion: {query}"}
        ]
    )
    answer=response.choices[0].message.content
    conn=sqlite3.connect("chat_history.db") 
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history(question,answer) VALUES (?,?)",
        (query,answer)
    )
    conn.commit()
    conn.close()
    return {"question":query,"answer":answer}