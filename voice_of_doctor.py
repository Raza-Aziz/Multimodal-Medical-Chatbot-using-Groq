import os
import platform
import subprocess
from gtts import gTTS
from dotenv import load_dotenv
import elevenlabs
from pydub import AudioSegment
from elevenlabs.client import ElevenLabs

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def text_to_speech_with_gtts(input_text, output_filepath):
    language = 'en'

    audio_obj = gTTS(
        text=input_text,
        lang=language,
        slow=False,
    )

    audio_obj.save(output_filepath)

def convert_mp3_to_wav(mp3_filepath, wav_filepath):
    audio = AudioSegment.from_mp3(mp3_filepath)
    audio.export(wav_filepath, format="wav")

def text_to_speech_with_elevenlabs(input_text, output_filepath): 
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    if not isinstance(input_text, str) or not input_text.strip():
        raise ValueError("Invalid text for speech synthesis. Ensure input_text is a valid string.")

    audio = client.generate(
        text=input_text,
        voice="IKne3meq5aSn9XLyUdCD",   # Charlie or George
        output_format="mp3_22050_32"
    )

    elevenlabs.save(audio, output_filepath)

    # Convert MP3 to WAV
    wav_filepath = output_filepath.replace(".mp3", ".wav")
    convert_mp3_to_wav(output_filepath, wav_filepath)

    os_name = platform.system()
    try:
        match os_name:
            case "Darwin":
                subprocess.run(['afplay', wav_filepath])
            case "Windows":
                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'])
            case "Linux":
                subprocess.run(['aplay', wav_filepath])
            case _:
                raise OSError("Unsupported Operating System")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")