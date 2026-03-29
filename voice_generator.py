from gtts import gTTS

def generate_voice(script_text):
    tts = gTTS(text=script_text, lang='en')

    output_path = "assets/voice.mp3"
    tts.save(output_path)

    return output_path