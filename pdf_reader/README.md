# 📖 PDF Reader Module

Minimal PDF reader for the Zera chatbot using RAG (Retrieval-Augmented Generation).

## Features

- 📤 Upload PDF files
- 🔍 Ask questions about PDF content
- 🗣️ Text-to-speech for answers
- ⚡ Fast similarity search using FAISS
- 🧠 Powered by Ollama models

## Usage

```python
from pdf_reader import PDFReader

# Initialize
pdf_reader = PDFReader()

# Load PDF
status = pdf_reader.load_pdf("document.pdf")
print(status)  # ✅ PDF loaded: 25 pages, 156 chunks

# Ask question
answer = pdf_reader.ask("What is the main topic?")
print(answer)  # Based on PDF content...

# Clear
pdf_reader.reset()
```

## Configuration

- **Embedding Model:** `nomic-embed-text` (vector creation)
- **LLM Model:** `zera` (question answering)
- **Vector DB:** FAISS (similarity search)
- **Chunk Size:** 800 characters
- **Chunk Overlap:** 100 characters
- **Retrieval:** Top 2 similar chunks

## File Structure

```
pdf_reader/
├── reader.py          # PDFReader class
├── pdf_utils.py       # Helper functions
├── __init__.py        # Module exports
├── db/                # Vector database (auto-generated)
└── README.md          # This file
```

## Requirements

```
langchain>=0.3.27
langchain-ollama>=0.3.7
langchain-community>=0.3.0
faiss-cpu>=1.8.0
ollama>=0.5.3
```

## Setup

1. Pull embedding model:
   ```bash
   ollama pull nomic-embed-text
   ```

2. Start Ollama:
   ```bash
   ollama serve
   ```

3. Use in Streamlit app:
   Toggle "📖 PDF Reader" in sidebar and upload a PDF!

## API Reference

### PDFReader

#### `__init__(db_path="pdf_reader/db", embed_model="nomic-embed-text", llm_model="zera")`
Initialize PDF reader with custom paths and models.

#### `load_pdf(pdf_path: str) -> str`
Load and process PDF file. Returns status message.

#### `ask(question: str) -> str`
Ask a question about the loaded PDF. Returns answer.

#### `reset()`
Clear loaded PDF and vector database.

## Tips

- Use longer PDFs for better context (10+ pages recommended)
- Ask specific questions for more accurate answers
- Vector DB is stored locally for fast reuse
- Each new PDF replaces the previous one
