import streamlit as st
from langchain_ollama import OllamaLLM
from spech import speak
from weapia_seaech import wiki_summary  # your Wikipedia function

# ✅ Initialize Ollama
llm = OllamaLLM(model="zera")   # replace with your model name

# --- Streamlit UI ---
st.set_page_config(page_title="Chatbot with Voice", page_icon="🤖")
st.title("🤖 Chatbot with Voice")
st.write("Type below and I’ll reply with text + speech.")

# --- Sidebar controls ---
st.sidebar.header("⚙️ Options")
use_wiki = st.sidebar.checkbox("🔎 Use Online Search ")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input (always stays at bottom)
user_input = st.chat_input("Say something...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("thinking..."):
        context = ""
        if use_wiki:
            wiki_info = wiki_summary(user_input, sentences=6)
            if not wiki_info.startswith("Error"):
                context = f"\n\nWikipedia says:\n{wiki_info}\n\n"

        # Final prompt with context
        final_prompt = f"""
        You are a helpful assistant.
        {context}
        User asked: "{user_input}"
        Provide a clear and concise answer.
        """
        response = llm.invoke(final_prompt)

    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Speak
    speak(response)

# --- Show chat history ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
