from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
pdf_path="Python Crash Course.pdf"
loader=PyPDFLoader(pdf_path)
documents=loader.load()
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
) 
chunks=text_splitter.split_documents(documents)
print(f"Total Chunks Created:{len(chunks)}")
print("---")
print("First Chunk Content")
print(chunks[0].page_content)
print("---")
print("second Chunk content")
print(chunks[1].page_content)