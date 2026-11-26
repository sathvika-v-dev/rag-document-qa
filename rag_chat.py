import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from groq import Groq
import sqlite3
# loading apikey from .env
load_dotenv()
groq_client=Groq(api_key=os.getenv("GROQ_API_KEY"))
#step1 :load embedding model and vector store
embedding_model=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vector_store=Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)
#step2:user question
query="what is this story about?"
#step3:retrieve relevantchunks
results=vector_store.similarity_search(query,k=2)
context="\n\n".join([doc.page_content for doc in results])
#step4:prompting
prompt=f""" Answer the question based only on the context
{context}
Question:{query}
Answer:"""
response=groq_client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role":"user","content":prompt}
    ]
)
print("Question:",query)
print("---")
print("Answer:",response.choices[0].message.content)

conn=sqlite3.connect("chat_history.db")
cursor=conn.cursor()
cursor.execute(
    "INSERT INTO Chat_history(question,answer)VALUES(?,?)",
    (query,response.choices[0].message.content)
    )
conn.commit()
conn.close()    