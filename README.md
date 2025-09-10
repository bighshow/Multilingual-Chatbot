# 🎙️ Multilingual RAG Voice Chatbot

A fully functional **Retrieval-Augmented Generation (RAG) chatbot** with **voice input/output capabilities** that allows you to interact with your PDF documents through natural conversation.

## 🌟 Key Features

- **🎤 Voice Input**: Speak your questions using Whisper speech-to-text
- **🔊 Voice Output**: Listen to responses with gTTS text-to-speech
- **📚 Document Intelligence**: Upload PDFs and get contextual answers using RAG
- **⚡ Fast Responses**: Redis caching for improved performance
- **🌍 Multilingual**: Support for multiple languages
- **💬 Interactive UI**: Clean Streamlit interface with chat history
- **🧠 Smart Retrieval**: ChromaDB vector search for relevant document chunks

## 🏗️ Architecture

```
User Input (Voice/Text) → Whisper STT → ChromaDB Retrieval → Gemini LLM → gTTS → Audio Output
                                    ↓
                              Redis Cache ← Document Embeddings (PDF)
```

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **LLM** | Google Gemini (Generative AI) |
| **Vector Database** | ChromaDB with Sentence Transformers |
| **Caching** | Redis |
| **Speech-to-Text** | OpenAI Whisper |
| **Text-to-Speech** | Google Text-to-Speech (gTTS) |
| **Web Interface** | Streamlit |
| **Document Processing** | PyPDF2 |
| **Embeddings** | Sentence Transformers |

## 📁 Project Structure

```
multilingual-rag-chatbot/
├── chatbot.py              # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (API keys)
├── .env.example          # Example environment file
├── README.md             # Project documentation
├── data/                 # Directory for PDF documents
│   └── sample.pdf       # Sample PDF for testing
├── chroma_db/           # ChromaDB vector store (auto-generated)
└── temp_audio/          # Temporary audio files (auto-generated)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Redis server
- Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/bighshow/Multilingual-Chatbot.git
cd Multilingual-Chatbot
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

**To get your Gemini API key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into your `.env` file

### 5. Start Redis Server

Make sure Redis is running on your system:

```bash
# On Linux/Mac with Homebrew:
redis-server

# On Ubuntu/Debian:
sudo systemctl start redis-server

# On Windows (if using Redis for Windows):
redis-server.exe
```

### 6. Run the Application

```bash
streamlit run chatbot.py
```

The application will open in your default browser at `http://localhost:8501`.

## 📖 How to Use

### 1. Upload Documents
- Place your PDF files in the `data/` directory
- The application will automatically process and embed them into ChromaDB

### 2. Ask Questions
- **Text Input**: Type your question in the text box
- **Voice Input**: Click the 🎤 microphone button and speak your question

### 3. Get Responses
- **Text Response**: View the answer in the chat interface
- **Audio Response**: Listen to the spoken response (auto-plays)

### 4. Supported Languages
- English
- Spanish
- French
- German
- Italian
- Portuguese
- And many more (depending on gTTS support)

## ⚙️ Configuration

### Customizing the Application

Edit `chatbot.py` to modify:

```python
# Document processing settings
CHUNK_SIZE = 1000           # Size of text chunks for embedding
CHUNK_OVERLAP = 200         # Overlap between chunks
TOP_K_RESULTS = 5          # Number of relevant chunks to retrieve

# Voice settings
TTS_LANGUAGE = 'en'        # Default TTS language
WHISPER_MODEL = 'base'     # Whisper model size (tiny, base, small, medium, large)

# Caching settings
CACHE_TTL = 3600          # Cache time-to-live in seconds
```

## 🔧 Advanced Setup

### Custom PDF Directory

```python
# In chatbot.py, modify the PDF path:
PDF_PATH = "path/to/your/document.pdf"
```

### Redis Configuration

For remote Redis or custom settings:

```env
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-password
REDIS_DB=0
```

## 📋 Requirements

### System Requirements
- Python 3.8+
- Redis server
- Internet connection (for Gemini API and gTTS)
- Microphone (for voice input)
- Speakers/headphones (for voice output)

### Python Dependencies
```txt
streamlit>=1.28.0
openai-whisper>=20231117
gtts>=2.4.0
chromadb>=0.4.15
redis>=5.0.0
sentence-transformers>=2.2.2
google-generativeai>=0.3.0
PyPDF2>=3.0.1
python-dotenv>=1.0.0
numpy>=1.24.0
```

## 🐛 Troubleshooting

### Common Issues

**1. Redis Connection Error**
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG
```

**2. Gemini API Key Error**
- Verify your API key in the `.env` file
- Check API quotas in Google AI Studio
- Ensure the API key has proper permissions

**3. Audio Issues**
- Check microphone permissions in your browser
- Ensure speakers/headphones are working
- Try refreshing the Streamlit app

**4. PDF Processing Errors**
- Ensure PDF files are not corrupted
- Check file permissions
- Verify PDF contains extractable text

### Performance Optimization

**For better performance:**
- Use SSD storage for ChromaDB
- Increase Redis memory allocation
- Use faster Whisper models for real-time processing
- Implement batch processing for multiple PDFs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Format code
black chatbot.py

# Lint code
flake8 chatbot.py
```


## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition
- Google for Gemini AI and gTTS
- ChromaDB team for the vector database
- Streamlit for the web framework
- Sentence Transformers for embeddings

