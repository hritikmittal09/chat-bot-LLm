
import streamlit as st
import threading
from pathlib import Path

# --- Imports ---
from Coding.Client import coding_agent_client
from langchain_ollama import OllamaLLM
from utils.spech import speak
from weapia_seaech import wiki_summary
from news import news
from File_Explore import getShortcutsList, openFile
from utils.voice_input import user_voiceInput
from Uicomponents.clock import sidebar_timer

# ✅ Initialize Ollama
llm = OllamaLLM(model="zera")

# --- Page Config ---
st.set_page_config(page_title="Chatbot with Voice", page_icon="🤖")
st.title("🤖 zera Chatbot with Voice")
st.write("Type below and I’ll reply with text + speech.")

# --- Sidebar ---
st.sidebar.header("⚙️ Options")
use_wiki = st.sidebar.checkbox("🔎 Use Online Search ")
listen_news = st.sidebar.toggle("📰 Listen News")
dev_mode = st.sidebar.toggle("🛠 Dev Mode (Coding Agent Only)")

fileExplor = st.sidebar.selectbox("File Explorer", [''] + getShortcutsList())
openFile(fileExplor)

sidebar_timer()

# =========================
# 📂 Upload Helper
# =========================
def save_uploaded_file(uploaded_file):
    upload_dir = Path("Upload")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


# =========================
# 🛠 Dev Mode UI
# =========================
uploaded_file = None

if dev_mode:
    st.sidebar.subheader("🛠 Coding Agent Tools")

    uploaded_file = st.sidebar.file_uploader("Upload file")

    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file)
        st.session_state["current_file"] = file_path
        st.sidebar.success(f"Uploaded: {file_path}")

    # Show uploaded files
    st.sidebar.write("📂 Uploaded Files:")
    for f in Path("Upload").glob("*"):
        st.sidebar.text(f.name)


# =========================
# 🎙 Voice Input (Disabled in Dev Mode)
# =========================
voice_input_text = None

if not dev_mode and st.sidebar.button("🎙 Voice Input"):
    st.sidebar.write("🎤 Listening...")
    voice_input_text = user_voiceInput()
    if not voice_input_text:
        st.sidebar.warning("⚠️ Could not capture voice.")


# =========================
# 💬 Session State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "speaking_news" not in st.session_state:
    st.session_state.speaking_news = False

if "news_buffer" not in st.session_state:
    st.session_state.news_buffer = None


# =========================
# 📰 News Feature (Disabled in Dev Mode)
# =========================
def fetch_and_speak_news(callback):
    try:
        titles = news()
        if not titles:
            callback("⚠️ No news found.")
            return

        news_text = "Here are the latest news:\\n\\n" + "\\n".join([f"- {t}" for t in titles])
        callback(news_text)

        st.session_state.speaking_news = True
        for t in titles:
            if not st.session_state.speaking_news:
                break
            speak(t)

    except Exception as e:
        callback(f"❌ Error: {e}")


def update_news_buffer(text):
    st.session_state.news_buffer = text


if not dev_mode and listen_news:
    if not st.session_state.speaking_news and st.session_state.news_buffer is None:
        with st.spinner("📰 Fetching news..."):
            threading.Thread(
                target=fetch_and_speak_news,
                args=(update_news_buffer,),
                daemon=True
            ).start()
else:
    st.session_state.speaking_news = False


# Add news to chat
if st.session_state.news_buffer:
    st.session_state.messages.append({
        "role": "assistant",
        "content": st.session_state.news_buffer
    })
    st.session_state.news_buffer = None


# =========================
# 💬 Chat Input
# =========================
user_input = st.chat_input("Say something...")

if not user_input and voice_input_text:
    user_input = voice_input_text


# =========================
# 🤖 Main Logic
# =========================
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):

        # ✅ DEV MODE → Coding Agent Only
        if dev_mode:
            try:
                response = coding_agent_client(user_input)
            except Exception as e:
                response = f"❌ Coding Agent Error: {e}"

        # ✅ NORMAL MODE → Ollama + Features
        else:
            context = ""
            if use_wiki:
                wiki_info = wiki_summary(user_input, sentences=6)
                if not wiki_info.startswith("Error"):
                    context = f"\\n\\nWikipedia says:\\n{wiki_info}\\n\\n"

            final_prompt = f"""
            You are a helpful assistant.
            {context}
            User asked: "{user_input}"
            Provide a clear and concise answer.
            """

            response = llm.invoke(final_prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})

    # 🔊 Speak only in normal mode
    if not dev_mode:
        speak(response)


# =========================
# 📄 File Preview + Download (DEV MODE)
# =========================
if dev_mode and "current_file" in st.session_state:
    file_path = st.session_state["current_file"]

    if file_path.exists():
        st.subheader("📄 File Preview")
        try:
            st.code(file_path.read_text())
        except:
            st.warning("Cannot preview binary file.")

        with open(file_path, "rb") as f:
            st.download_button(
                label="⬇️ Download Modified File",
                data=f,
                file_name=file_path.name,
                mime="application/octet-stream"
            )


# =========================
# 💬 Chat Display
# =========================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

