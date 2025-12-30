import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

# ================= CONFIG =================
USER_NAME = "Naman"
WAKE_WORD = "hey namo"
genai.configure(api_key="AIzaSyDBZGWbOOL6ntypSLorl2ebdcD_rwM_21w")

# ================= TEXT TO SPEECH =================
engine = pyttsx3.init()
engine.setProperty("rate", 170)

voices = engine.getProperty("voices")

def speak(text, emotion="neutral"):
    if emotion == "happy":
        engine.setProperty("rate", 180)
        engine.setProperty("voice", voices[1].id)
    elif emotion == "serious":
        engine.setProperty("rate", 150)
        engine.setProperty("voice", voices[0].id)
    else:  # neutral
        engine.setProperty("rate", 170)

    engine.say(text)
    engine.runAndWait()

# ================= SPEECH TO TEXT =================
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio).lower()
    except:
        return ""

# ================= EMOTION DETECTION =================
def detect_emotion(text):
    happy_words = ["great", "awesome", "nice", "good", "happy"]
    serious_words = ["problem", "issue", "important", "serious", "help"]

    if any(word in text for word in happy_words):
        return "happy"
    if any(word in text for word in serious_words):
        return "serious"
    return "neutral"

# ================= GEMINI MODEL =================
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=(
        "You are a friendly AI voice assistant. "
        "Reply in medium-length answers only. "
        "Keep responses clear and conversational. "
        "Do not give long explanations. "
        "Address the user by name when appropriate."
    )
)

chat = model.start_chat(history=[])

# ================= START ASSISTANT =================
print("🎧 Voice Assistant running...")
print(f"Say '{WAKE_WORD}' to activate.")

speak(f"Voice assistant started. Say {WAKE_WORD} to begin.")

active = False

# ================= CONTINUOUS LISTENING =================
while True:
    heard = listen()

    if not heard:
        continue

    print("Heard:", heard)

    # Wake word detection
    if not active and WAKE_WORD in heard:
        active = True
        speak(f"Yes {USER_NAME}, I am listening.")
        continue

    # Ignore everything until wake word is spoken
    if not active:
        continue

    # Exit command
    if "exit" in heard or "stop" in heard or "quit" in heard:
        speak(f"Goodbye {USER_NAME}. Have a great day.")
        break

    # Emotion detection
    emotion = detect_emotion(heard)

    # Gemini response
    response = chat.send_message(heard)
    reply = response.text

    print("Chatbot:", reply)
    speak(reply, emotion=emotion)

# ================= END =================
print("🎧 Voice Assistant shutting down...")