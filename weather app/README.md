Atmosphere Weather App

A minimalist, desktop-based weather dashboard built with Python.

I built this project to practice integrating REST APIs with a graphical user interface (GUI). Instead of using standard API keys that expire, I implemented a two-step fetching process using Open-Meteo to resolve city names to coordinates and then fetch live weather data.

Features

No API Key Required: Utilizes Open-Meteo for hassle-free data fetching.

Smart Search: Implements a Geocoding step to convert city names (e.g., "London") into precise Latitude/Longitude coordinates.

Clean UI: Custom dark theme designed with Tkinter, focusing on readability and minimalism.

Error Handling: Robust checks for network issues or invalid city names to prevent crashes.

Tech Stack

Language: Python 3.x

GUI: Tkinter (Standard Python Library)

HTTP Requests: requests library

API: Open-Meteo

How to Run

Clone the repository (or download the files):

git clone [https://github.com/yourusername/atmosphere-weather.git](https://github.com/yourusername/atmosphere-weather.git)
cd atmosphere-weather


Install the dependencies:
The only external library required is requests.

pip install requests


Run the application:

python weather_dashboard.py


Project Structure

weather_dashboard.py: Main application logic containing both the frontend (UI) and backend (API) functions.

README.md: Project documentation.

Future Improvements

If I were to expand this project, I would look into:

Adding a 7-day forecast view.

Saving the user's "last searched" city to a local config file.

Adding a toggle for Celsius/Fahrenheit.
