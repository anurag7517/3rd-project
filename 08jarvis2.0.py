import speech_recognition as sr
import edge_tts
import asyncio
from playsound import playsound
import os
import webbrowser 
import time
import datetime
import pywhatkit as kit

r = sr.Recognizer() 

async def speak_async(text):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-JennyNeural"
    )
    await communicate.save("voice.mp3")

def speak(text):
    asyncio.run(speak_async(text))
    playsound("voice.mp3")
    time.sleep(0.5)
    os.remove("voice.mp3")


def processcommand(c):
    c = c.lower() 

    if "search google for" in c:
        query = c.replace("search google for", "").strip()
        speak(f"searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "google" in c:
        webbrowser.open("https://google.com") 

    elif "youtube" in c:
        webbrowser.open("https://youtube.com") 

    elif "time" in c:
        time_now = datetime.datetime.now().strftime("%H:%M")
        speak(f"the time is {time_now}")

    elif "date" in c:
        date_now = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"today's date is {date_now}")
    
    elif "play song" in c:
        song = c.replace("play song", "").strip()
        speak(f"playing {song}")
        kit.playonyt(song)
 
if __name__ == "__main__":
    speak("Initializing alpha") 

    while True:
       #listen for the wake word jarvis
       #obtain audio drom the microphone

       print("Recognizing...")
    
       try:
           with sr.Microphone() as source: 
             r.adjust_for_ambient_noise(source, duration=1)
             print("Listening...") 
             audio = r.listen(source, timeout=10, phrase_time_limit=7)
           word = r.recognize_google(audio)
           print("Heard:", word)

           if "alpha" in word.lower():
              audio = None
              time.sleep(1)
              speak("yes anurag sir")

              # listen for command 
              with sr.Microphone() as source: 
                 r.adjust_for_ambient_noise(source, duration=1)
                 print("alpha active") 
                 audio = r.listen(source, timeout=10, phrase_time_limit=7)
                 command = r.recognize_google(audio)
                 print("Command:", command)

                 processcommand(command)
                 
           
       except Exception as e:
        print(f"Error: {e}")
        speak("say that again anurag sir")
        

       

