import speech_recognition as sr
import time
import os
import keyboard
from dotenv import load_dotenv
load_dotenv()
rec = sr.Recognizer()
def print_microphone():
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone {i}: {microphone_name}")

def loop(source):
    while True:
        key = os.getenv("ACTIVATE_KEY")
        if keyboard.is_pressed(key):
            print("Listening...")
            audio = rec.listen(source)
            result = call_openai(audio)
            print(f"You Said: {result}")
            keyboard.write(result)
            if result: break
        time.sleep(0.1)
    loop(source)
def call_openai(audio):
    
    try:
        text = rec.recognize_openai(audio)
        return text

    except sr.UnknownValueError:
        print("Whisper Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper Speech Recognition service; {0}".format(e))

def main():
    if os.getenv("OPENAI_API_KEY") == "":
        raise Exception("OPENAI_API_KEY environment variable is not set. Please set it in .env file... See .env.example")
        return
    with sr.Microphone(device_index=int(os.getenv("USE_MICROPHONE_INDEX"))) as source:
        rec.adjust_for_ambient_noise(source, duration=int(os.getenv("AMBIENT_NOISE_DURATION")))
    
        loop(source)

if __name__ == "__main__":
    if os.getenv("LIST_MICROPHONE_ON_START") == "Y":
        print_microphone()
    main()


