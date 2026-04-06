from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

# Create embeddings
embeddings = HuggingFaceEmbeddings()

def create_vectorstore(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = text_splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


def get_rag_answer(query, text):
    # simple RAG logic
    if query.lower() in text.lower():
        return text[:1000]
    else:
        return text[:1000]