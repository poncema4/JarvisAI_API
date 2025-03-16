import speech_recognition as sr
import pyttsx3
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Function to speak the text
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# Initialize speech recognizer
r = sr.Recognizer()

def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                print("I'm listening...")

                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2).lower()
                print("What you said: "+ MyText)
                
                if "goodbye" in MyText:
                    print("Goodbye! Terminating the program...")
                    SpeakText("Goodbye! Have a nice day.")
                    exit()

                return MyText
    
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

        except sr.UnknownValueError:
            print("Unknown error occurred")

def send_to_chatgpt(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100,
        temperature=0.5,
    )

    message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": message})
    return message

messages = []
while True:
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_chatgpt(messages)
    SpeakText(response)
    print("Reponse: " + response)
