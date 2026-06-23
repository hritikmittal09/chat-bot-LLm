import streamlit as st
import threading
import queue
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
from pdf_reader import PDFReader
#from tools.weather import get_weather
#from tools.websearch import web_search
from ollama import chat
from tools.tool_call import tool_map
from tools.tools_schema import tools_schemas

# ✅ Initialize Ollama
llm = OllamaLLM(model="zera")
listen_news = False

# Global variables for thread communication
news_queue = queue.Queue()
speaking = False

# --- Page Config ---
st.set_page_config(page_title="Chatbot with Voice", page_icon="🤖")
st.title("🤖 zera Chatbot with Voice")
st.write("Type below and I’ll reply with text + speech.")

# --- Sidebar ---
st.sidebar.header("⚙️ Options")
#use_wiki = st.sidebar.checkbox("🔎 Use Online Search ")
#listen_news = st.sidebar.toggle("📰 Listen News")
dev_mode = st.sidebar.toggle("🛠 Dev Mode (Coding Agent Only)")
pdf_mode = st.sidebar.toggle("📖 PDF Reader")

fileExplor = st.sidebar.selectbox("File Explorer", [''] + getShortcutsList())
openFile(fileExplor)

#sidebar_timer() # TODO timer is not working disabling for noow


def speak_in_bg(text):
    """Speak text in background thread"""
    st.session_state.speaking = True
    speak(text)
    st.session_state.speaking = False


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
# 📖 PDF Reader Mode
# =========================
if pdf_mode:
    st.sidebar.subheader("📖 PDF Reader")
    
    pdf_file = st.sidebar.file_uploader("Upload PDF", type=["pdf"], key="pdf_upload")
    
    if pdf_file:
        # Save and load PDF
        pdf_path = save_uploaded_file(pdf_file)
        result = st.session_state.pdf_reader.load_pdf(str(pdf_path))
        st.session_state.pdf_loaded = True
        st.sidebar.info(result)
    
    if st.session_state.pdf_loaded and st.sidebar.button("🗑️ Clear PDF"):
        st.session_state.pdf_reader.reset()
        st.session_state.pdf_loaded = False
        st.rerun()


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

if "pdf_reader" not in st.session_state:
    st.session_state.pdf_reader = PDFReader()
    st.session_state.pdf_loaded = False

if "speaking" not in st.session_state:
    st.session_state.speaking = False


# =========================
# 📰 News Feature (Disabled in Dev Mode)
# =========================
def fetch_and_speak_news():
    global speaking
    try:
        titles = news()
        if not titles:
            news_queue.put("⚠️ No news found.")
            return

        news_text = "Here are the latest news:\\n\\n" + "\\n".join([f"- {t}" for t in titles])
        news_queue.put(news_text)

        speaking = True
        for t in titles:
            if not speaking:
                break
            speak(t)

    except Exception as e:
        news_queue.put(f"❌ Error: {e}")


if not dev_mode and listen_news:
    if not speaking and news_queue.empty():
        with st.spinner("📰 Fetching news..."):
            threading.Thread(
                target=fetch_and_speak_news,
                daemon=True
            ).start()
else:
    speaking = False


# Process news from queue
if not news_queue.empty():
    text = news_queue.get()
    st.session_state.messages.append({
        "role": "assistant",
        "content": text
    })
    st.rerun()


# =========================
# 💬 Chat Input
# =========================
if pdf_mode:
    if st.session_state.pdf_loaded:
        user_input = st.chat_input("Ask question about PDF...")
    else:
        st.warning("⚠️ Upload a PDF first")
        user_input = None
else:
    user_input = st.chat_input("Say something...")

if not user_input and voice_input_text:
    user_input = voice_input_text


# =========================
# 🤖 Main Logic
# =========================
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):

        # ✅ PDF MODE → Ask PDF
        if pdf_mode and st.session_state.pdf_loaded:
            response = st.session_state.pdf_reader.ask(user_input)

        # ✅ DEV MODE → Coding Agent Only
        elif dev_mode:
            try:
                response = coding_agent_client(user_input)
            except Exception as e:
                response = f"❌ Coding Agent Error: {e}"

        # ✅ NORMAL MODE → Ollama + Tools
        else:
            tools = tools_schemas

            messages = [{"role": "user", "content": user_input}]
            response = chat(model="zera", messages=messages, tools=tools)

            # Handle tool calls
            if response.message.tool_calls:
                for tool_call in response.message.tool_calls:
                    name = tool_call.function.name
                    args = tool_call.function.arguments
                    print(f"calling tool {name} eith args {args} ....")


                    tool_result = tool_map[name](args)
                    messages.append({"role": "assistant", "content": response.message.content, "tool_calls": [tool_call]})
                    messages.append({"role": "tool", "content": str(tool_result)})
                #print(messages)
                response = chat(model="zera", messages=messages, tools=tools)    
                  

            response = response.message.content

    st.session_state.messages.append({"role": "assistant", "content": response})

    # 🔊 Speak in background thread (non-blocking for all modes)
    threading.Thread(
        target=speak_in_bg,
        args=(response,),
        daemon=True
    ).start()


# =========================
# 🔊 Speaking Indicator
# =========================
if st.session_state.speaking:
    st.sidebar.info("🔊 Speaking...")


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

