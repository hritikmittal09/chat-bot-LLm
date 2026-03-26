import streamlit as st
from Coding.Client import coding_agent_client
import threading
from langchain_ollama import OllamaLLM
from utils.spech import speak
from weapia_seaech import wiki_summary  # your Wikipedia function
from news import news
from File_Explore import getShortcutsList, openFile
from utils.voice_input import user_voiceInput
from Uicomponents.clock import sidebar_timer


# ✅ Initialize Ollama
llm = OllamaLLM(model="zera")   # replace with your model name

# --- Streamlit UI ---
st.set_page_config(page_title="Chatbot with Voice", page_icon="🤖")
st.title("🤖 zera Chatbot with Voice")
st.write("Type below and I’ll reply with text + speech.")

# --- Sidebar controls ---
st.sidebar.header("⚙️ Options")
use_wiki = st.sidebar.checkbox("🔎 Use Online Search ")
listen_news = st.sidebar.toggle("📰 Listen News")
dev_mode = st.sidebar.toggle("turn on dev mode")


fileExplor = st.sidebar.selectbox("File Explorer", [''] + getShortcutsList())
openFile(fileExplor)

sidebar_timer()


# 🎙 Voice Input Button
voice_input_text = None
if st.sidebar.button("🎙 Voice Input"):
    st.sidebar.write("🎤 Listening...")
    voice_input_text = user_voiceInput()
    if not voice_input_text:
        st.sidebar.warning("⚠️ Could not capture voice. Please try again.")


# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "speaking_news" not in st.session_state:
    st.session_state.speaking_news = False
if "news_buffer" not in st.session_state:
    st.session_state.news_buffer = None   # temporary buffer for thread results


# --- Background task for fetching & speaking news ---
def fetch_and_speak_news(callback):
    try:
        titles = news()  # should return list of titles
        if not titles:
            callback("⚠️ No news found.")
            return

        news_text = "Here are the latest news headlines:\n\n" + "\n".join([f"- {t}" for t in titles])
        callback(news_text)  # update session state safely

        # Speak headlines one by one
        st.session_state.speaking_news = True
        for t in titles:
            if not st.session_state.speaking_news:  # stop if toggle off
                break
            speak(t)

    except Exception as e:
        callback(f"❌ Error fetching news: {e}")


# --- Safe updater for session state ---
def update_news_buffer(text):
    st.session_state.news_buffer = text


# --- Handle Listen News toggle ---
if listen_news:
    if not st.session_state.speaking_news and st.session_state.news_buffer is None:
        with st.spinner("📰 Fetching news..."):
            threading.Thread(
                target=fetch_and_speak_news,
                args=(update_news_buffer,),
                daemon=True
            ).start()
else:
    st.session_state.speaking_news = False

# --- If thread placed something in buffer, add to messages ---
if st.session_state.news_buffer:
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.news_buffer})
    st.session_state.news_buffer = None  # clear buffer so it doesn’t repeat


# --- Chat input (text + voice merged here) ---
user_input = st.chat_input("Say something...")
if not user_input and voice_input_text:  # if no text but voice exists
    user_input = voice_input_text

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("thinking..."):
        context = ""
        if use_wiki:
            wiki_info = wiki_summary(user_input, sentences=6)
            if not wiki_info.startswith("Error"):
                context = f"\n\nWikipedia says:\n{wiki_info}\n\n"

        final_prompt = f"""
        You are a helpful assistant.
        {context}
        User asked: "{user_input}"
        Provide a clear and concise answer.
        """
        response = llm.invoke(final_prompt)

    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Speak response
    speak(response)


# --- Show chat history ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
