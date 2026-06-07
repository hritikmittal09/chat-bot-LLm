"""
Minimal PDF Reader Module
Uploads PDF, processes it, and answers questions using Zera model
"""
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from .pdf_utils import (
    load_pdf,
    split_pdf,
    create_embeddings,
    save_vectorstore,
    load_vectorstore
)
from .config import (
    EMBEDDING_MODEL,
    LLM_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    RETRIEVAL_K,
    DB_PATH,
    ERROR_NO_PDF,
    SUCCESS_LOADED
)
import os
import shutil


class PDFReader:
    def __init__(self, db_path=DB_PATH, embed_model=EMBEDDING_MODEL, llm_model=LLM_MODEL):
        """Initialize PDF Reader with vector database path"""
        self.db_path = db_path
        self.embed_model = embed_model
        self.llm_model = llm_model
        self.vectorstore = None
        self.qa = None
        
    def load_pdf(self, pdf_path):
        """Load PDF and create vector database"""
        try:
            # Load PDF
            documents = load_pdf(pdf_path)
            pages = len(documents)
            
            # Split into chunks
            chunks = split_pdf(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
            
            # Create embeddings
            self.vectorstore, _ = create_embeddings(chunks, model=self.embed_model)
            
            # Create QA chain with Zera model
            llm = OllamaLLM(model=self.llm_model)
            self.qa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": RETRIEVAL_K})
            )
            
            # Save to disk
            save_vectorstore(self.vectorstore, self.db_path)
            
            return SUCCESS_LOADED.format(pages=pages, chunks=len(chunks))
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def ask(self, question):
        """Ask question about PDF"""
        if self.qa is None:
            return ERROR_NO_PDF
        
        try:
            response = self.qa.invoke({"query": question})
            return response.get("result", "No answer found")
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def reset(self):
        """Clear loaded PDF"""
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
        self.vectorstore = None
        self.qa = None

