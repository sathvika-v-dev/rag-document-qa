import os
import tempfile
import uuid

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


st.title("RAG DOCUMENT Q&A")
st.write("Upload a PDF and ask questions about it")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None and st.session_state.get("file_name") != uploaded_file.name:
    with st.spinner("Processing PDF..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        pages = PyPDFLoader(tmp_path).load()
        os.remove(tmp_path)
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(pages)
        st.session_state["vector_store"] = Chroma.from_documents(
            chunks,
            load_embeddings(),
            collection_name=f"docs_{uuid.uuid4().hex}",
        )
        st.session_state["file_name"] = uploaded_file.name
    st.success("PDF processed. You can ask questions now.")

question = st.text_input("Enter your question")

if st.button("Ask"):
    if "vector_store" not in st.session_state:
        st.write("Please upload a PDF first")
    elif question:
        with st.spinner("Thinking..."):
            docs = st.session_state["vector_store"].similarity_search(question, k=2)
            context = "\n\n".join(d.page_content for d in docs)
            response = groq_client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that answers questions based only on the provided context.",
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {question}",
                    },
                ],
            )
            answer = response.choices[0].message.content
        st.write(answer)
    else:
        st.write("Please enter a question")