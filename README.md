# RAG Document Q&A System

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their content. The system retrieves relevant information from the document and generates accurate, context-aware answers using an LLM.

## Features
- Upload any PDF document
- Ask natural language questions about the document
- Get AI-generated answers based on document content
- Chat history stored in a SQL database

## Tech Stack
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **LLM:** Groq (Llama 3.1)
- **Embeddings:** HuggingFace Sentence Transformers
- **Vector Database:** ChromaDB
- **Database:** SQLite
- **Framework:** LangChain

## How It Works
1. User uploads a PDF document
2. The document is split into smaller chunks
3. Each chunk is converted into embeddings (vector representations)
4. Embeddings are stored in a vector database (ChromaDB)
5. When a user asks a question, the system retrieves the most relevant chunks
6. The relevant context is passed to an LLM (Groq) to generate a natural language answer
7. The question and answer are saved to a SQL database

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
python -m venv venv
venv\Scripts\activate
3. Install dependencies:
pip install -r requirements.txt
4. Add your Groq API key to a `.env` file:
GROQ_API_KEY=your_key_here
5. Run the FastAPI backend:
uvicorn api:app --reload
6. Run the Streamlit frontend (in a new terminal):
streamlit run app_ui.py

## Future Improvements
- Support for multiple document formats (Word, TXT)
- Multi-document querying
- Improved prompt engineering for more accurate responses