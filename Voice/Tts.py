import threading
import pyttsx3

from Config import TTS_ENGINE



def _speak_pyttsx3(text: str):
    try:
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')

        
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)

        engine.setProperty('rate', 175)
        engine.setProperty('volume', 1.0)

        print(f"[pyttsx3] Speaking: {text}")

        engine.say(text)
        engine.runAndWait()

        engine.stop()

    except Exception as e:
        print(f"[pyttsx3 ERROR] {e}")



def speak(text: str, blocking: bool = True):

    if not text or text.strip() == "":
        return

    if blocking:
        _speak_pyttsx3(text)

    else:
        threading.Thread(
            target=_speak_pyttsx3,
            args=(text,),
            daemon=True
        ).start()