"""
PDF QNA - Helper functions for PDF processing
"""
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
import os
import shutil


def load_pdf(pdf_path):
    """Load and split PDF into chunks"""
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents


def split_pdf(documents, chunk_size=800, chunk_overlap=100):
    """Split PDF documents into chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(documents)


def create_embeddings(chunks, model="nomic-embed-text"):
    """Create embeddings for chunks"""
    embeddings = OllamaEmbeddings(model=model)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore, embeddings


def save_vectorstore(vectorstore, db_path):
    """Save vector store to disk"""
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
    vectorstore.save_local(db_path)


def load_vectorstore(db_path, model="nomic-embed-text"):
    """Load vector store from disk"""
    embeddings = OllamaEmbeddings(model=model)
    vectorstore = FAISS.load_local(
        db_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore
