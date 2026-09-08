from langchain_community.document_loaders import PyPDFLoader
pdf_path="Python Crash Course.pdf"

loader=PyPDFLoader(pdf_path)
documents=loader.load()
print(f"Total pages loaded:{len(documents)}")
print("---")
print("First Page Content preview")
print(documents[0].page_content[:500])