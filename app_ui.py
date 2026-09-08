import streamlit as st
import requests
st.title("RAG Document Project")
st.write("Ask questions about your document")
uploaded_file=st.file_uploader("Upload a PDF",type="pdf")
if uploaded_file is not None:
    if st.button("Process PDF"):
        files={"file":(uploaded_file.name,uploaded_file.getvalue(),"application/pdf")}
        upload_response=requests.post("http://127.0.0.1:8000/upload",files=files)
        if upload_response.status_code==200:
            st.success(upload_response.json()["message"])
        else:
            st.error("Failed to process PDF")    
question=st.text_input("Enter your Question")
if st.button("Ask"):
    if question:
        response=requests.post(
            "http://127.0.0.1:8000/ask",
            json={"question":question}
        )
        if response.status_code==200:
            answer=response.json()["answer"]
            st.write(answer)
        else:
            st.write("Error:Could not get response")    
    else:
        st.write("please enter a question")        