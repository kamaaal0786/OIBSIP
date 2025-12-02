# **🌤️ Atmosphere Weather App**

A clean, minimalist desktop weather application built with Python.

I created this project to explore **GUI development** and **API chaining**. Unlike standard weather apps that require complex API keys, this tool uses a custom logic flow to fetch data seamlessly using Open-Meteo.

## **🚀 Key Features**

* **No API Keys Needed:** Built on the Open-Meteo architecture, allowing the app to run immediately without user configuration.  
* **Two-Step Data Fetching:**  
  1. **Geocoding:** Converts city names (e.g., "Tokyo") into precise Latitude/Longitude coordinates.  
  2. **Meteorology:** Uses coordinates to fetch live weather data.  
* **Modern UI:** A custom dark-themed interface built with Tkinter, moving away from the default "gray" system look.  
* **Resilient Error Handling:** The app manages network timeouts and invalid city names gracefully without crashing.

## **🛠️ Tech Stack**

* **Language:** Python 3.10+  
* **Interface:** Tkinter (Standard Library)  
* **Networking:** Requests (pip install requests)  
* **Data Source:** [Open-Meteo API](https://open-meteo.com/)

## **💻 How to Run This Project**

1. **Clone the repository:** 

2. Install dependencies:  
   This project is lightweight and only requires one external package.  
   pip install requests

3. **Run the app:**  
   python weather.py

## **📂 Project Structure**

* weather.py \- The main entry point. Contains the UI rendering logic and the API fetch functions.  
* README.md \- Documentation.

## **🔮 Future Improvements**

If I continue working on this, I plan to add:

* **7-Day Forecast:** Displaying a list of future weather conditions.  
* **Unit Toggle:** A switch for Celsius/Fahrenheit.  
* **Local Caching:** Saving the last searched city so it loads automatically on startup.

*Built for my Internship Portfolio.*