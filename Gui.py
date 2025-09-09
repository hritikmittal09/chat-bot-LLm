import streamlit as st
from langchain_ollama import OllamaLLM
from spech import speak
from weapia_seaech import wiki_summary  # your Wikipedia function
from news import news
import threading

# ✅ Initialize Ollama
llm = OllamaLLM(model="zera")   # replace with your model name

# --- Streamlit UI ---
st.set_page_config(page_title="Chatbot with Voice", page_icon="🤖")
st.title("🤖 Chatbot with Voice")
st.write("Type below and I’ll reply with text + speech.")

# --- Sidebar controls ---
st.sidebar.header("⚙️ Options")
use_wiki = st.sidebar.checkbox("🔎 Use Online Search ")
listen_news = st.sidebar.toggle("📰 Listen News")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "speaking_news" not in st.session_state:
    st.session_state.speaking_news = False
if "news_buffer" not in st.session_state:
    st.session_state.news_buffer = None   # temporary buffer for thread results

# --- Function to fetch & speak news ---
def fetch_and_speak_news():
    try:
        titles = news()  # should return list of titles
        if not titles:
            st.session_state.news_buffer = "⚠️ No news found."
            return

        news_text = "Here are the latest news headlines:\n\n" + "\n".join([f"- {t}" for t in titles])
        st.session_state.news_buffer = news_text  # store in buffer

        # Speak headlines one by one
        st.session_state.speaking_news = True
        for t in titles:
            if not st.session_state.speaking_news:  # stop if toggle off
                break
            speak(t)

    except Exception as e:
        st.session_state.news_buffer = f"❌ Error fetching news: {e}"

# --- Handle Listen News toggle ---
if listen_news:
    if not st.session_state.speaking_news and st.session_state.news_buffer is None:
        with st.spinner("📰 Fetching news..."):
            threading.Thread(target=fetch_and_speak_news, daemon=True).start()
else:
    st.session_state.speaking_news = False

# --- If thread placed something in buffer, add to messages ---
if st.session_state.news_buffer:
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.news_buffer})
    st.session_state.news_buffer = None  # clear buffer so it doesn’t repeat

# --- Chat input ---
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
