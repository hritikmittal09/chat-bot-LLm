from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
import os
path = "test.pdf"
print(os.path.exists(path))  # sh

# 1. Load PDF
path = r"D:\chatbot\test.pdf" # change if your PDF name is different
loader = PyPDFLoader(path)
documents = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,   # max chars per chunk
    chunk_overlap=100  # keep some context between chunks
)
docs = splitter.split_documents(documents)

print(f"✅ PDF split into {len(docs)} chunks")

# 3. Create embeddings using Ollama
embeddings = OllamaEmbeddings(model="zera")   # using your local model

# 4. Store in FAISS (local vector DB)
vectorstore = FAISS.from_documents(docs, embeddings)

# 5. Save to disk
vectorstore.save_local("vector_db")

print("✅ Vector DB created and saved in 'vector_db' folder")
