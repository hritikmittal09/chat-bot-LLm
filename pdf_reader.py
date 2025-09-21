import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from spech import speak


class PDFChatbot:
    def __init__(self, pdf_path: str, model_name: str = "zera"):
        """Initialize with a PDF path and build vector DB"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"❌ File not found: {pdf_path}")

        self.pdf_path = pdf_path
        self.model_name = model_name

        # Step 1: Load PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        print(f"✅ Loaded {len(documents)} pages from PDF")

        # Step 2: Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        docs = splitter.split_documents(documents)
        print(f"✅ PDF split into {len(docs)} chunks")

        # Step 3: Embeddings
        embeddings = OllamaEmbeddings(model=model_name)

        # Step 4: Store in FAISS
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local("vector_db")
        print("✅ Vector DB created and saved in 'vector_db' folder")

        # Step 5: Setup Retriever + LLM
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        llm = OllamaLLM(model=model_name)

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff"
        )

    def ask(self, query: str, speak_out: bool = False) -> str:
        """Ask a question and get the answer"""
        answer = self.qa_chain.run(query)
        if speak_out:
            speak(answer)
        return answer


if __name__ == "__main__":
    chatbot = PDFChatbot(r"test.pdf", model_name="zera")

    print("\n🤖 PDF QnA Chatbot Ready! Type 'quit' to exit.\n")
    while True:
        query = input("You: ")
        if query.lower() in ["quit", "exit"]:
            print("👋 Goodbye!")
            break
        response = chatbot.ask(query, speak_out=True)
        print(f"Bot: {response}\n")
