

import time
import speech_recognition as sr

from Stt import record_and_transcribe
from Brain import ask_friday
from Tts import speak
from Config import RECORD_SECONDS, WAKE_WORDS


STARTUP_MESSAGE = "Hey! I'm awake and listening to you."


SLEEP_WORDS = ["stop", "bye", "goodbye", "sleep", "go to sleep", "that's all"]

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True



def listen_for_wake_word() -> bool:
    """
    Listens passively in short bursts.
    Returns True only when a wake word is heard.
    """
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
        except sr.WaitTimeoutError:
            return False

    try:
        heard = recognizer.recognize_google(audio).lower()
        print(f"[Wake] Heard: '{heard}'")
        for word in WAKE_WORDS:
            if word in heard:
                return True
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        print("[Wake] Google STT unavailable, retrying...")

    return False



def listen_for_command() -> str:
    
    print("[Friday] Listening for your command...")
    text = record_and_transcribe()
    return text.strip() if text else ""



def is_sleep_command(text: str) -> bool:
    """Returns True if the user wants Friday to go back to sleep."""
    text_lower = text.lower()
    for word in SLEEP_WORDS:
        if word in text_lower:
            return True
    return False



def run():
    print("=" * 50)
    print("  F.R.I.D.A.Y.  —  Phase 1 Voice Loop")
    print("=" * 50)
    print(f"Silent boot. Waiting for wake word: {WAKE_WORDS}")
    print("=" * 50 + "\n")

    while True:
        try:
            
            print("[Mode] Sleeping — say 'Hey Friday' to wake me up...")
            wake_detected = listen_for_wake_word()

            if not wake_detected:
                continue  

            
            print("\n[Friday] Wake word detected! Entering active mode.")
            speak(STARTUP_MESSAGE)   

            
            print("[Mode] Active — talk freely. Say 'bye' to put me to sleep.\n")

            while True:
                
                text = listen_for_command()

                if not text:
                    speak("I didn't catch that. Go ahead.")
                    continue

                print(f"[You]     {text}")

                
                if is_sleep_command(text):
                    speak("Going to sleep. Say Hey Friday whenever you need me.")
                    print("[Mode] Going back to sleep...\n")
                    break  

                
                print("[Friday]  Thinking...")
                reply = ask_friday(text)
                print(f"[Friday]  {reply}\n")
                speak(reply)

            

        except KeyboardInterrupt:
            print("\n[Friday] Shutting down. Goodbye.")
            speak("Shutting down. Goodbye.")
            break

        except Exception as e:
            print(f"[Error] {e}")
            time.sleep(1)
            continue


if __name__ == "__main__":
    run()