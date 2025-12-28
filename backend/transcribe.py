import whisper

# Load the Whisper speech-to-text model once at startup
# "base" is a good balance between speed and accuracy
model = whisper.load_model("base")

def transcribe_audio(audio_path):
    """
    Takes an audio file path and returns:
    1. Original transcription (original language)
    2. English translation

    This runs completely locally (no API calls).
    """

    # Transcribe audio in its original language
    result = model.transcribe(audio_path)
    original_text = result["text"]

    # Translate audio into English
    translated = model.transcribe(audio_path, task="translate")
    translated_text = translated["text"]

    # Return both results
    return original_text.strip(), translated_text.strip()
