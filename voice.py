import speech_recognition as sr
import pyttsx3

# 🔊 TTS ENGINE
engine = pyttsx3.init()
engine.setProperty('rate', 220)
engine.setProperty('volume', 1.0)

is_speaking = False


# 🔊 SPEAK (FIXED)
# voice.py mein ye update karo
def speak(text):
    global is_speaking
    try:
        is_speaking = True
        print("nova:", text)
        
        # Bolne se pehle engine ko reset karo taaki naya command turant suna ja sake
        engine.stop() 
        engine.say(text)
        engine.runAndWait()
        
        is_speaking = False
    except Exception as e:
        print("Speak Error:", e)
        is_speaking = False


# 🛑 STOP SPEAKING
def stop_speaking():
    global is_speaking
    is_speaking = False
    engine.stop()


# 🎤 TAKE COMMAND
def take_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)

            command = recognizer.recognize_google(audio)
            print("You:", command)

            return command.lower()

        except:
            return ""