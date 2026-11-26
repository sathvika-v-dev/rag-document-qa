from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
#step1:pdfload
pdf_path="Python Crash Course.pdf"
loader=PyPDFLoader(pdf_path)
documents=loader.load()
#step2: creating chunks 
text_splitter=RecursiveCharacterTextSplitter(
    chunk_overlap=50,
    chunk_size=500
)
chunks=text_splitter.split_documents(documents)
print(f"Total Chunks:{len(chunks)}")

#step3:embedding model loading and vector_store
embedding_model=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vector_store=Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma_db"
)
#step4:test 
query="what is this document about?"
results=vector_store.similarity_search(query,k=2)
print("---")
print("Query:",query)
print("---")
print("Top matching chunk:")
print(results[0].page_content)