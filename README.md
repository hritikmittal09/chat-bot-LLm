# 🤖 Zera Virtual Assistant Project

---

## 📌 Project Overview

**Version:** 0.1.0  
**Description:**  
**Zera** is an intelligent, voice-enabled AI chatbot powered by **Ollama** and **LangChain**, featuring real-time text-to-speech, knowledge retrieval, and an elegant **Streamlit** web interface.  
It can chat naturally, read responses aloud, and dynamically fetch information from the web and Wikipedia.

**Readme:** README.md  
**Python Requirement:** >=3.13  

This project is a chatbot powered by **Ollama** with **text-to-speech**, **LangChain** integrations, and a **Streamlit UI**.

---

## 📦 Dependencies

The project uses the following dependencies:

| Dependency | Version | Purpose |
|-------------|----------|----------|
| `edge-tts` | >=7.2.3 | For text-to-speech conversion (Edge TTS) |
| `langchain` | >=0.3.27 | Core LangChain library for building LLM-powered apps |
| `langchain-ollama` | >=0.3.7 | Integration of LangChain with Ollama models |
| `langchain-community` | >=0.3.0 | Community integrations for LangChain |
| `faiss-cpu` | >=1.8.0 | Vector similarity search for PDF QNA |
| `newsapi-python` | >=0.2.7 | Fetch real-time news articles |
| `ollama` | >=0.5.3 | Ollama LLM runtime |
| `pyinstaller` | >=6.15.0 | Package app into executable format |
| `python-dotenv` | >=1.1.1 | Manage environment variables |
| `pyttsx3` | >=2.99 | Offline text-to-speech engine |
| `streamlit` | >=1.49.1 | Web-based UI for the chatbot |
| `wikipedia` | >=1.4.0 | Retrieve knowledge from Wikipedia |

---

![alt text](image.png)

---

## 🚀 Installation

### Using [uv](https://github.com/astral-sh/uv) (Recommended)

```bash
# 1️⃣ Create a virtual environment
uv venv

# 2️⃣ Activate the environment
source .venv/bin/activate   # For Mac/Linux
.venv\Scripts\activate      # For Windows PowerShell

# 3️⃣ Install all dependencies
uv pip install -r pyproject.toml
```

---

## 🧠 Model Setup (Ollama)

1. **Install Ollama**  
   Download from the official site → [https://ollama.ai/download](https://ollama.ai/download)

2. **Verify Installation**
   ```bash
   ollama --version
   ```

3. **Create the Zera Model**  
   Go to the `config/` folder which contains your Ollama model file (e.g., `zera_model.ollama`), then run:
   ```bash
   ollama create zera -f config/zera_model.ollama
   ```

4. **Test the Model**
   ```bash
   ollama run zera
   ```

5. **Pull the Embedding Model (for PDF Reader)**
   ```bash
   ollama pull nomic-embed-text
   ```

6. **Start Ollama Server**
   ```bash
   ollama serve
   ```

---

## 📖 PDF Reader Mode

**New Feature:** Upload PDFs and ask questions about them using **RAG (Retrieval-Augmented Generation)**!

### How to Use:

1. **Toggle PDF Reader** in the sidebar: "📖 PDF Reader"
2. **Upload a PDF** using the file uploader
3. **Wait for processing** (text is split into chunks and embedded)
4. **Ask questions** about the PDF content
5. **Zera answers** based on PDF context (with text-to-speech)

### Technical Details:

- **Embedding Model:** `nomic-embed-text` (dedicated embeddings)
- **LLM:** `zera` model answers questions
- **Vector DB:** FAISS for fast similarity search
- **Chunk Size:** 800 characters with 100-char overlap
- **Retrieval:** Top 2 relevant chunks per question

### File Structure:
```
pdf_reader/
├── reader.py      # PDFReader class
└── __init__.py    # Module exports

Storage:
├── pdf_reader/db/     # Vector database (auto-created)
└── Upload/            # Uploaded PDFs
```

---

## 🔑 Environment Setup

1. Duplicate `.env.example` → rename it to `.env`  
2. Add your API keys and configurations inside `.env`:
   ```env
   news_api_key=your_news_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   MODEL=your_model_name_here
   ```

---

## 🗂️ File Explorer Setup

Zera supports a **File Explorer** feature that lets you open apps and websites directly by voice or chat command.

### Step 1: Create `filepaths.json`

In the **root of your project**, create a file named `filepaths.json` and add your desired app paths and URLs:

```json
{
  "Spotify": "C:\\Users\\Lenovo\\AppData\\Roaming\\Spotify\\Spotify.exe",
  "YouTube": "https://www.youtube.com/",
  "Linked-in": "https://www.linkedin.com/feed/",
  "Naukri": "https://www.naukri.com/mnjuser/homepage",
  "Indeed": "https://in.indeed.com/",
  "leetcode": "https://leetcode.com/problemset/",
  "hacktoberfest": "https://hacktoberfest.com/profile/",
  "coursera-rag": "https://www.coursera.org/learn/retrieval-augmented-generation-rag/"
}
```

> 💡 **Tips:**
> - For **desktop apps** → use the full `.exe` path (Windows) or app path (Mac/Linux)
> - For **websites** → use the full URL starting with `https://`
> - Use double backslashes `\\` for Windows paths
> - Key names are case-insensitive when Zera searches them

---

### Step 2: How Zera Uses It

Zera reads `filepaths.json` at startup and maps each key to its path. When you say or type something like:

```
User: Open Spotify
User: Open YouTube
User: Open leetcode
```

Zera will:
- **Desktop apps** → launch the `.exe` directly using `subprocess` or `os.startfile`
- **URLs** → open in your default browser using `webbrowser.open()`

---

### Step 3: Add More Entries Anytime

Simply edit `filepaths.json` and add a new line:

```json
{
  "GitHub": "https://github.com/",
  "VS Code": "C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
}
```

No restart needed if Zera reloads the file dynamically.

---

### 📁 File Explorer: Project Structure

```
zera/
├── filepaths.json          # ← Your app & URL shortcuts
├── modules/
│   └── file_explorer.py    # ← Handles open commands
└── ...
```

---

## ▶️ Run the Application

Once all dependencies and models are ready, start the chatbot:
```bash
python main.py
```

Then open the local Streamlit app (usually: [http://localhost:8501](http://localhost:8501))  
Enjoy chatting with **Zera – Your Personal AI Assistant** 🎙️🤖

---

## 💻 Usage

Once running, **Zera** can:
- 🗣️ Talk with you using natural speech (Edge TTS or pyttsx3).  
- 💬 Respond intelligently using Ollama's LLM models.  
- 🌐 Fetch live news or knowledge using NewsAPI and Wikipedia.  
- 🗂️ Open apps and websites via the File Explorer feature.  
- 🎨 Provide a clean, interactive UI with Streamlit.  

Example commands:
```
User: What's the latest news about AI?
Zera: Fetching the most recent updates from trusted sources...

User: Open Spotify
Zera: Opening Spotify for you! 🎵

User: Open leetcode
Zera: Launching LeetCode in your browser! 💻
```

---

## 🛠️ Zera Ollama Tool Features

**Zera** is equipped with powerful Ollama-integrated tools that extend its capabilities beyond conversation. These tools enable the AI to perform real-world tasks autonomously.

### 🌍 Web & Information Tools

#### 1. **Web Search** 🔍
- **Purpose:** Search the internet for real-time information
- **When Used:** Current events, recent news, product information, trending topics
- **Integration:** Uses DuckDuckGo Search via LangChain
- **Example:**
  ```
  User: What's the latest news about AI advancements?
  Zera: [Searches the web] Here are the latest developments...
  ```

#### 2. **Weather Information** ⛅
- **Purpose:** Get real-time weather data for any city
- **API:** wttr.in (Free weather API)
- **Details Provided:** Current temperature, conditions, wind, humidity
- **Example:**
  ```
  User: What's the weather in London?
  Zera: [Fetches weather data] The weather in London is...
  ```

---

### 📁 File System Tools

Zera can read, write, and manage files in the **upload/** working directory.

#### 3. **Get File Content** 📄
- **Purpose:** Read and display file contents
- **Limit:** First 10,000 characters (truncated for long files)
- **Supported:** .txt, .md, .json, .py, .csv, and more
- **Example:**
  ```
  User: Read the file notes.txt
  Zera: [Reads file] Here's the content...
  ```

#### 4. **Get File Info** ℹ️
- **Purpose:** List files and folder structure
- **Retrieves:** File names, types, sizes, and directory listings
- **Example:**
  ```
  User: What files are in the upload folder?
  Zera: [Lists files] I found the following files...
  ```

#### 5. **Get Folder Content** 📂
- **Purpose:** Explore directory structure recursively
- **Shows:** All subdirectories and files with organization
- **Example:**
  ```
  User: Show me the folder structure
  Zera: [Maps directory] Here's the complete structure...
  ```

#### 6. **Write File** ✍️
- **Purpose:** Create or modify text files
- **Location:** Files are saved in the **upload/** directory
- **Example:**
  ```
  User: Create a file called summary.txt with "Hello World"
  Zera: [Creates file] File saved successfully!
  ```

#### 7. **Make Directory** 📁
- **Purpose:** Create new folders in the working directory
- **Example:**
  ```
  User: Create a folder called "projects"
  Zera: [Creates directory] Folder created successfully!
  ```

#### 8. **Run Python File** 🐍
- **Purpose:** Execute Python scripts directly
- **Safety:** Runs only scripts in the **upload/** directory
- **Output:** Returns script execution results
- **Example:**
  ```
  User: Run the analysis.py script
  Zera: [Executes script] Script output: ...
  ```

---

### 📚 Knowledge Tools

#### 9. **PDF Reader with RAG** 📖
- **Purpose:** Extract information from PDF documents
- **Technology:** Retrieval-Augmented Generation (RAG)
- **How It Works:**
  1. Upload PDF → Zera processes and embeds the text
  2. Ask Questions → Zera retrieves relevant sections
  3. Get Answers → Based on PDF context with AI reasoning
- **Vector DB:** FAISS for fast similarity search
- **Example:**
  ```
  User: [Uploads research_paper.pdf] Summarize the findings
  Zera: [Retrieves relevant sections] The key findings are...
  ```

#### 10. **Wikipedia Search** 🔎
- **Purpose:** Retrieve encyclopedia knowledge
- **Used For:** Historical facts, general knowledge, explanations
- **Example:**
  ```
  User: Tell me about the French Revolution
  Zera: [Searches Wikipedia] The French Revolution was...
  ```

#### 11. **News API** 📰
- **Purpose:** Fetch real-time news articles
- **Requires:** `news_api_key` in `.env` file
- **Coverage:** Global news sources and topics
- **Example:**
  ```
  User: Latest news about technology
  Zera: [Fetches from NewsAPI] Here are top stories...
  ```

---

### 🎯 How Zera Chooses Tools

Zera uses **intelligent tool selection** via Ollama's function calling:

1. **Analyzes your request** → Understands the intent
2. **Selects appropriate tool(s)** → Weather, Web Search, File ops, etc.
3. **Executes with context** → Passes parameters intelligently
4. **Synthesizes response** → Combines tool results with reasoning
5. **Speaks the answer** → Uses text-to-speech for delivery

**Example Multi-Tool Flow:**
```
User: "Create a file with today's weather in Paris and top tech news"

Zera:
  1. Uses Weather Tool → Gets Paris weather data
  2. Uses Web Search Tool → Fetches latest tech news
  3. Uses Write File Tool → Creates results.txt
  4. Speaks confirmation → "Done! Created file with info."
```

---

### ⚙️ Tool Configuration

Tools are defined in two main files:

**[tools/tools_schema.py](tools/tools_schema.py)** - Function schemas for Ollama  
**[tools/tool_call.py](tools/tool_call.py)** - Function execution mapping

To add a new tool:
1. Create the function in `tools/`
2. Add schema definition in `tools_schema.py`
3. Map execution in `tool_call.py`
4. Include in Ollama prompt context

---

---

## 🧰 Project Structure

```
zera/
├── config/
│   ├── zera_model.ollama        # Ollama model definition
│   └── settings.env.example     # Example environment file
├── filepaths.json               # App & URL shortcuts for File Explorer
├── main.py                      # Entry point for the app
├── modules/
│   ├── speech_engine.py         # Text-to-speech logic
│   ├── llm_handler.py           # Ollama + LangChain integration
│   ├── news_fetcher.py          # Fetch latest news
│   ├── wiki_handler.py          # Wikipedia search utility
│   └── file_explorer.py         # File Explorer / app launcher
├── requirements.txt / pyproject.toml
├── README.md
└── .env
```

---

## 🧩 Features

✅ **Voice-enabled conversations**  
✅ **Offline and online speech synthesis**  
✅ **LangChain-powered reasoning**  
✅ **Dynamic web + Wikipedia knowledge retrieval**  
✅ **File Explorer — open apps & websites by voice**  
✅ **Clean Streamlit UI**  
✅ **Cross-platform support (Windows / Mac / Linux)**  

---

## 🏗️ Build Executable (Optional)

To package the app as a standalone executable:

```bash
pyinstaller --noconfirm --onefile --windowed main.py
```

The build output will be in the `dist/` folder.

---

## 🧑‍💻 Author

**Hritik Mittal**  
💼 Full Stack Developer | AI & Automation Enthusiast  
🌐 [GitHub](https://github.com/hritikmittal09)

---

## 🪪 License

This project is licensed under the **MIT License** — you're free to use, modify, and distribute it with attribution.

---

*Zera – Speak. Learn. Connect.* ⚡