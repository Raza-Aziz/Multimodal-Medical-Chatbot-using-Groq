# Basic
import os 
import logging
from dotenv import load_dotenv
from groq import Groq  

# For speech and voice processing
import speech_recognition as sr  # Audio recording and speech recognition
from pydub import AudioSegment  # Audio format conversion
from io import BytesIO  # For handling in-memory byte streams

# Load environment variables from .env file (contains GROQ_API_KEY)
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')  # Retrieve API key from environment variables

# Configure logging to show timestamps and message severity
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """Records audio from microphone and saves as MP3 file.
    
    Args:
        file_path (str): Path to save recorded audio
        timeout (int): Maximum recording time in seconds
        phrase_time_limit (int): Max duration for single speech segment
    """
    recognizer = sr.Recognizer()
    device_index = 1  # Specific microphone index (Realtek Audio in this case)
    
    # --For debugging microphone list: 
    # print(sr.Microphone().list_microphone_names())

    try:
        with sr.Microphone(device_index=device_index) as source:
            logging.info("Adjusting for ambient noise...")
            # Reduce background noise interference (1 second sample)
            recognizer.adjust_for_ambient_noise(source, duration=1)

            # Start recording audio from microphone
            logging.info("Start speaking now...")
            audio_data = recognizer.listen(source, timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete...")

            # Convert audio to MP3 format
            wav_data = audio_data.get_wav_data()  # Get raw WAV data
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))  # Create audio segment
            # Export as MP3 with 128kbps bitrate
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            logging.info(f"Audio saved at {file_path}")
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def transcribe_with_groq(stt_model, audio_file_path, GROQ_API_KEY):
    # Initialize Groq client with API key
    client = Groq(api_key=GROQ_API_KEY)
    # Specify speech-to-text model (Whisper large V3)
    stt_model = "whisper-large-v3"
    # Open recorded audio file in read-binary mode
    audio_file = open(audio_file_path, "rb")

    # Transcribe audio using Groq's Whisper model
    transcription = client.audio.transcriptions.create(
        model=stt_model,  # Speech-to-text model to use
        file=audio_file,  # Audio file to transcribe
        language="en"  # Specify audio language (English)
    )

    return transcription.text