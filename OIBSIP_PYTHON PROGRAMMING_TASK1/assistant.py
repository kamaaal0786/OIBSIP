import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import os
import pyjokes
import time
import tkinter as tk
from tkinter import scrolledtext
import threading

# GUI Globals
window = None
console = None

def log(text):
    # Updates the text box in the GUI
    if console:
        console.configure(state='normal')
        console.insert(tk.END, text + "\n")
        console.configure(state='disabled')
        console.see(tk.END)
    print(text)

def speak(text):
    log(f"Assistant: {text}")

    # Re-initialize engine to avoid crashing loop
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) 
    engine.setProperty('rate', 175)
    
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    speak("I am online. How can I help?")

def listen_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        log("\nListening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        log("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        log(f"User said: {query}")
    except Exception:
        return "None"
    return query

def open_site(url):
    # Try to open in Chrome, fallback to default
    path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    try:
        webbrowser.get(path).open(url)
    except:
        log("Chrome not found, using default browser.")
        webbrowser.open(url)

def get_notepad_path():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_path, "todo_list.txt")

def save_note(text):
    path = get_notepad_path()
    try:
        with open(path, "a") as f:
            now = datetime.datetime.now().strftime("%I:%M %p")
            f.write(f"[{now}] {text}\n")
        log(f"Saved to {path}")
    except Exception:
        speak("I couldn't save that note.")

def assistant_loop():
    greet_user()
    
    while True:
        query = listen_input().lower()

        if query == "none":
            continue

        # --- Logic Handlers ---

        if 'open spotify' in query or 'play music' in query:
            speak("Opening Spotify Web Player...")
            time.sleep(0.1)
            open_site("open.spotify.com")

        elif 'open youtube' in query:
            speak("Opening YouTube")
            time.sleep(0.1)
            open_site("youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            time.sleep(0.1)
            open_site("google.com")
            
        elif 'open stackoverflow' in query:
            speak("Opening Stack Overflow")
            time.sleep(0.1)
            open_site("stackoverflow.com")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")    
            speak(f"The time is {strTime}")

        elif 'the date' in query or 'todays date' in query:
            strDate = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today's date is {strDate}")

        # Note taking loop
        elif 'make a note' in query or 'make to do list' in query or 'add to list' in query:
            speak("What should I write? Say 'stop' or 'done' to finish.")
            
            while True:
                note = listen_input().lower()
                
                if note == "none":
                    continue

                if 'stop' in note or 'done' in note or 'that is all' in note:
                    speak("Okay, list saved.")
                    break
                
                save_note(note)
                speak("Added. Anything else?")

        elif 'show my list' in query or 'show list' in query:
            path = get_notepad_path()
            if os.path.exists(path):
                speak("Opening your list.")
                os.startfile(path)
            else:
                speak("You haven't made a list yet.")

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'stop' in query or 'exit' in query:
            speak("Goodbye!")
            if window:
                window.destroy()
            break

def start_app():
    t = threading.Thread(target=assistant_loop)
    t.daemon = True
    t.start()

# --- GUI Construction ---
if __name__ == "__main__":
    window = tk.Tk()
    window.title("Python Voice Assistant")
    window.geometry("800x500")
    window.configure(bg="#1e1e1e")

    lbl = tk.Label(window, text="VOICE ASSISTANT", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white")
    lbl.pack(pady=15)

    console = scrolledtext.ScrolledText(window, width=90, height=20, font=("Consolas", 10), bg="black", fg="#00ff00")
    console.pack(pady=10, padx=10)
    console.configure(state='disabled')

    btn = tk.Button(window, text="START ASSISTANT", command=start_app, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", height=2, width=20)
    btn.pack(pady=10)

    window.mainloop()