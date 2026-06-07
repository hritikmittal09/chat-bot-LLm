"""
PDF Reader Configuration and Constants
"""

# Model Configuration
EMBEDDING_MODEL = "nomic-embed-text"  # For creating embeddings
LLM_MODEL = "zera"                     # For answering questions

# PDF Processing
CHUNK_SIZE = 800          # Characters per chunk
CHUNK_OVERLAP = 100       # Overlap between chunks
RETRIEVAL_K = 2           # Number of chunks to retrieve

# Storage
DB_PATH = "pdf_reader/db"  # Vector database storage location
UPLOAD_PATH = "Upload"     # Uploaded PDF storage location

# Error Messages
ERROR_NO_PDF = "❌ No PDF loaded. Upload a PDF first."
ERROR_LOADING = "❌ Error loading PDF: {}"
ERROR_ANSWERING = "❌ Error answering question: {}"

# Success Messages
SUCCESS_LOADED = "✅ PDF loaded: {pages} pages, {chunks} chunks"
