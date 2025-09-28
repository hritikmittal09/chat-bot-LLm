from langchain_ollama import OllamaLLM
from utils. spech import speak
import os


def cmdbotTest():
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

def Run():
    

# Replace "cmd_command" with the actual command you want to run
    cmd_command = "streamlit run Gui.py"

# Execute the command using os.system()
    os.system(cmd_command)
if __name__ == "__main__":
    Run()

