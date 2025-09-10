

```markdown
# 🎙️ Multilingual RAG Voice Chatbot

A fully functional **Retrieval-Augmented Generation (RAG) chatbot** with **voice input/output**, built using:

- **Whisper** → Speech-to-Text (voice input)
- **gTTS** → Text-to-Speech (voice output)
- **ChromaDB** → Vector database for RAG
- **Redis** → Caching for faster responses
- **Gemini (Google Generative AI)** → LLM for response generation
- **Streamlit** → Interactive web interface
- **PDF ingestion** → Chat with your documents

---

## ✨ Features
- **Multimodal Input**: Ask questions via **voice** (Whisper) or **text**.  
- **Voice Output**: Answers are spoken back using **gTTS**.  
- **Document-Aware RAG**: Embeds PDF into **ChromaDB**, retrieves top-k relevant chunks, and feeds them to Gemini for precise answers.  
- **Caching with Redis**: Reduces repeated LLM calls and speeds up responses.  
- **Multilingual Support**: Handles multiple languages for queries and voice synthesis.  
- **Streamlit UI**: Chat interface with microphone button and audio playback.  

---

## 📂 Project Structure
```

.
├── chatbot.py          # Main Streamlit app
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .env                # Environment variables (API keys)

````

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/bighshow/Multilingual-Chatbot.git
cd Multilingual-Chatbot
````

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root with your **Gemini API key**:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

### 5. Run Redis (for caching)

Make sure you have Redis running locally:

```bash
redis-server
```

---

## ▶️ Usage

Start the chatbot:

```bash
streamlit run chatbot.py
```

1. Upload or configure your **PDF document** (path is set in `chatbot.py`).
2. Ask questions via:

   * **Text input box**
   * **🎤 Speak button** (voice input)
3. Get answers with:

   * **Text displayed in chat**
   * **Audio response played automatically**

---

## 🛠️ Tech Stack

* **LLM**: Gemini (Google Generative AI)
* **Vector DB**: ChromaDB + Sentence Transformers
* **Cache**: Redis
* **Speech-to-Text**: Whisper
* **Text-to-Speech**: gTTS
* **UI**: Streamlit
* **Docs**: PyPDF2 for PDF parsing

