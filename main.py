from langchain_ollama import OllamaLLM
from spech import speak

# ✅ Initialize Ollama with your model
llm = OllamaLLM(model="zera")   # replace with your model name

print("🤖 Chatbot Ready! Type 'quit' or 'exit' to stop.\n")

userInput = ""  # initialize variable

while userInput.lower() not in ["quit", "exit"]:
    userInput = input("You: ")
    if userInput.lower() in ["quit", "exit"]:
        print("👋 Goodbye!")
        break

    # ✅ Ask a question
    response = llm.invoke(userInput)
    print("thinking ...")

    print("Bot:", response)
    speak(response)
