import streamlit as st
import google.generativeai as genai
import PyPDF2
import os
from dotenv import load_dotenv
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import threading

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Specify the PDF path here
PDF_PATH = "C:\\Users\\Asus\\OneDrive\\Desktop\\chatbot\\plants.pdf"

# Initialize translator
translator = Translator()

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def detect_language(text):
    try:
        return translator.detect(text).lang
    except:
        return 'en'  # Default to English if detection fails

def translate_text(text, target_lang='en'):
    try:
        return translator.translate(text, dest=target_lang).text
    except:
        return text  # Return original text if translation fails

def ask_gemini(prompt, context, target_lang):
    model = genai.GenerativeModel('gemini-pro')
    
    # Translate prompt to English
    en_prompt = translate_text(prompt, 'en')
    
    try:
        response = model.generate_content(f"{context}\n\nQuestion: {en_prompt}")
        
        if response.candidates and response.candidates[0].content:
            # Extract the text from the response
            response_text = response.candidates[0].content.parts[0].text
            
            # Translate response back to target language
            translated_response = translate_text(response_text, target_lang)
            return translated_response
        else:
            # Handle case where response is empty
            error_message = "I'm sorry, but I couldn't generate a response. This might be due to safety filters or an empty response from the AI model."
            return translate_text(error_message, target_lang)
    except Exception as e:
        # Handle any other exceptions
        error_message = f"An error occurred: {str(e)}"
        return translate_text(error_message, target_lang)

def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

def play_audio(file_path):
    audio = AudioSegment.from_mp3(file_path)
    play(audio)
    os.unlink(file_path)  # Delete the temporary file

def main():
    st.set_page_config(page_title="Multilingual AshokVatika Chatbot", page_icon="🌳")
    
    st.title("Multilingual AshokVatika Chatbot")
    
    # Language selector
    languages = {
        'English': 'en',
        'Hindi': 'hi',
        'Bengali': 'bn',
        'Sanskrit': 'sa'
    }
    selected_language = st.selectbox("Select Language", list(languages.keys()))
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": translate_text("Hi I am Ashok. Welcome to AshokVatika. How may I assist you?", languages[selected_language])}
        ]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is your question?"):
        # Detect input language
        detected_lang = detect_language(prompt)
        
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Read PDF content (only once)
        if "pdf_content" not in st.session_state:
            st.session_state.pdf_content = read_pdf(PDF_PATH)

        response = ask_gemini(prompt, st.session_state.pdf_content, languages[selected_language])
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Generate and play audio response
        audio_file = text_to_speech(response, languages[selected_language])
        st.audio(audio_file, format='audio/mp3')

        # Play audio in background
        threading.Thread(target=play_audio, args=(audio_file,)).start()

if __name__ == "__main__":
    main()