# **🎙️ Desktop Voice Assistant**

A streamlined, efficient desktop voice assistant built with Python.

I created this project to explore **Speech Recognition** and **GUI Integration**. Unlike standard console-based scripts, this tool features a responsive graphical interface and threading logic to handle voice inputs without freezing the application.

## **🚀 Key Features**

* **Smart Voice Recognition:** Powered by Google's Speech Recognition API to accurately convert speech to text.  
* **Task Automation:**  
  1. **Web Control:** One-command access to Spotify, YouTube, Google, and StackOverflow.  
  2. **System Info:** Instantly fetches the current date and time.  
* **Persistent Notes:** A "Make a note" feature that saves your dictation to a local todo\_list.txt file automatically.  
* **Modern UI:** A custom dark-themed interface built with Tkinter, featuring a scrolling console log for real-time feedback.  
* **Threaded Performance:** Runs the listening loop on a background thread, ensuring the GUI remains smooth and responsive.

## **🛠️ Tech Stack**

* **Language:** Python 3.10+  
* **Interface:** Tkinter (Standard Library)  
* **Speech Engine:** SpeechRecognition & pyttsx3  
* **Concurrency:** Threading (Standard Library)

## **💻 How to Run This Project**

1. **Clone the repository** or download the files.  
2. Install dependencies:  
   Run the following command to install the required voice processing libraries:  
   pip install \-r requirements.txt

   *Note: On Windows, if you encounter issues with PyAudio, you may need to use pipwin install pyaudio.*  
3. **Run the app:**  
   python assistant.py

## **📂 Project Structure**

* assistant.py \- The main entry point. Contains the GUI setup, threading logic, and voice command handlers.  
* requirements.txt \- List of external Python libraries required.  
* todo\_list.txt \- (Auto-generated) Stores notes and to-do lists created via voice commands.  
* README.md \- Documentation.

## **🔮 Future Improvements**

If I continue working on this, I plan to add:

* **Wake Word Detection:** Listening for a specific phrase like "Hey Python" to start recording.  
* **Application Launching:** Opening specific desktop applications based on dynamic paths.  
* **Weather Integration:** fetching live weather data for the user's location.

*Built for my Internship Portfolio.*