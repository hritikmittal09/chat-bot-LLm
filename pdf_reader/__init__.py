"""PDF Reader Module - Upload PDFs and ask questions using RAG"""
from .reader import PDFReader
from .pdf_utils import load_pdf, split_pdf, create_embeddings, save_vectorstore, load_vectorstore
from .config import (
    EMBEDDING_MODEL,
    LLM_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    RETRIEVAL_K,
    DB_PATH
)

__all__ = [
    "PDFReader",
    "load_pdf",
    "split_pdf",
    "create_embeddings",
    "save_vectorstore",
    "load_vectorstore",
    "EMBEDDING_MODEL",
    "LLM_MODEL",
    "CHUNK_SIZE",
    "CHUNK_OVERLAP",
    "RETRIEVAL_K",
    "DB_PATH"
]
