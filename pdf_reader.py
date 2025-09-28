from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
import os
from utils. spech import speak


def pdf_reader(filepath = ''):# Path to your PDF
    path = r"D:\chatbot\test.pdf"

    # --- Step 1: Load PDF ---
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File not found: {path}")

    loader = PyPDFLoader(path)
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} pages from PDF")

    # --- Step 2: Split into chunks ---
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    docs = splitter.split_documents(documents)
    print(f"✅ PDF split into {len(docs)} chunks")

    # --- Step 3: Create embeddings ---
    embeddings = OllamaEmbeddings(model="zera")

    # --- Step 4: Store in FAISS ---
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("vector_db")
    print("✅ Vector DB created and saved in 'vector_db' folder")

    # --- Step 5: Setup QnA chain ---
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = OllamaLLM(model="zera")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )

    # --- Step 6: Interactive QnA ---
    print("\n🤖 PDF QnA Chatbot Ready! Type 'quit' to exit.\n")
    while True:
        query = input("You: ")
        if query.lower() in ["quit", "exit"]:
            print("👋 Goodbye!")
            break
        answer = qa_chain.run(query)
        print(f"Bot: {answer}\n")
        speak(answer)
    if __name__ == "__main__":
        pdf_reader()    
