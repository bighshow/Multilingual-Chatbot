import streamlit as st
import google.generativeai as genai
import os
import tempfile
import threading
import redis
import chromadb
from chromadb.utils import embedding_functions
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import whisper

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

redis_client = redis.Redis(host="localhost", port=6379, db=0)

chroma_client = chromadb.Client()
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="docs", embedding_function=embedding_function)

PDF_PATH = "C:\\Users\\Asus\\OneDrive\\Desktop\\chatbot\\plants.pdf"
whisper_model = whisper.load_model("base")

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def index_pdf():
    text = read_pdf(PDF_PATH)
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        collection.add(documents=[chunk], ids=[f"chunk_{i}"])

def retrieve_context(query, k=3):
    results = collection.query(query_texts=[query], n_results=k)
    return " ".join(results["documents"][0]) if results["documents"] else ""

def ask_gemini(prompt, context):
    cache_key = f"qa:{prompt}"
    cached = redis_client.get(cache_key)
    if cached:
        return cached.decode("utf-8")
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"{context}\n\nQuestion: {prompt}")
    if response.candidates and response.candidates[0].content:
        answer = response.candidates[0].content.parts[0].text
    else:
        answer = "I could not generate a response."
    redis_client.set(cache_key, answer)
    return answer

def text_to_speech(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

def play_audio(file_path):
    audio = AudioSegment.from_mp3(file_path)
    play(audio)
    os.unlink(file_path)

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
            wav_path = fp.name
            with open(wav_path, "wb") as f:
                f.write(audio.get_wav_data())
        result = whisper_model.transcribe(wav_path)
        os.remove(wav_path)
        return result["text"]

def main():
    st.set_page_config(page_title="RAG Voice Chatbot", page_icon="🎙️")
    st.title("Multilingual RAG Voice Chatbot")

    if "indexed" not in st.session_state:
        index_pdf()
        st.session_state.indexed = True

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi, I am your RAG assistant. How can I help you?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.button("🎤 Speak"):
        voice_input = speech_to_text()
        st.chat_message("user").markdown(voice_input)
        st.session_state.messages.append({"role": "user", "content": voice_input})
        context = retrieve_context(voice_input)
        response = ask_gemini(voice_input, context)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        audio_file = text_to_speech(response)
        st.audio(audio_file, format="audio/mp3")
        threading.Thread(target=play_audio, args=(audio_file,)).start()

    if prompt := st.chat_input("Type your question..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        context = retrieve_context(prompt)
        response = ask_gemini(prompt, context)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        audio_file = text_to_speech(response)
        st.audio(audio_file, format="audio/mp3")
        threading.Thread(target=play_audio, args=(audio_file,)).start()

if __name__ == "__main__":
    main()
