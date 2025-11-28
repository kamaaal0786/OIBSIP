import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

# --- Configuration ---
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# UI Colors
THEME = {
    "bg": "#2c2f33",
    "fg": "#ffffff",
    "accent": "#7289da",
    "sub": "#99aab5",
    "input": "#23272a"
}

# --- Logic ---

def get_icon(code):
    # Maps WMO codes to icons and text
    if code == 0: return "☀️", "Clear Sky"
    if code <= 3: return "⛅", "Partly Cloudy"
    if code in [45, 48]: return "🌫", "Foggy"
    if code in [51, 53, 55, 61, 63, 65]: return "🌧", "Rain"
    if code in [71, 73, 75, 77]: return "❄️", "Snow"
    if code >= 95: return "⛈", "Thunderstorm"
    return "🌥", "Overcast"

def get_data(city):
    """
    Fetches coordinates then weather. 
    Returns: (data_dict, error_message)
    """
    if not city:
        return None, "Please enter a city."

    try:
        # 1. Geocoding
        payload = {"name": city, "count": 1, "language": "en", "format": "json"}
        response = requests.get(GEO_URL, params=payload)
        geo_data = response.json()

        if "results" not in geo_data:
            return None, "City not found."

        loc = geo_data["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        name = loc["name"]
        country = loc.get("country_code", "").upper()

        # 2. Weather Data
        w_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "temperature_unit": "celsius",
            "windspeed_unit": "ms"
        }
        response = requests.get(WEATHER_URL, params=w_params)
        data = response.json()

        if "current_weather" in data:
            current = data["current_weather"]
            return {
                "temp": current["temperature"],
                "wind": current["windspeed"],
                "code": current["weathercode"],
                "city": name,
                "country": country
            }, None
        
        return None, "Weather unavailable."

    except Exception as e:
        return None, f"Connection Error: {e}"

def perform_search(event=None):
    city = entry_box.get()
    
    # Simple UI feedback
    btn_go.config(state=tk.DISABLED)
    data, error = get_data(city)
    btn_go.config(state=tk.NORMAL)

    if error:
        messagebox.showerror("Error", error)
    else:
        icon, desc = get_icon(data["code"])
        
        # Update UI
        lbl_temp.config(text=f"{icon} {data['temp']:.0f}°")
        lbl_desc.config(text=desc)
        lbl_loc.config(text=f"{data['city']}, {data['country']}")
        lbl_stats.config(text=f"Wind: {data['wind']} m/s")

# --- Main App ---

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Atmosphere")
    app.geometry("350x500")
    app.resizable(False, False)
    app.configure(bg=THEME["bg"])

    # Search Bar
    top_frame = tk.Frame(app, bg=THEME["bg"], pady=30)
    top_frame.pack()

    entry_box = tk.Entry(
        top_frame, font=("Segoe UI", 14), width=18, bd=0, 
        bg=THEME["input"], fg=THEME["fg"], 
        insertbackground=THEME["accent"], justify='center'
    )
    entry_box.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
    entry_box.focus()
    entry_box.bind('<Return>', perform_search)

    btn_go = tk.Button(
        top_frame, text="Go", font=("Segoe UI", 12, "bold"), 
        bg=THEME["accent"], fg=THEME["fg"], 
        activebackground=THEME["accent"], activeforeground=THEME["fg"],
        command=perform_search, relief=tk.FLAT, bd=0, padx=15, pady=2
    )
    btn_go.pack(side=tk.LEFT)

    # Results
    mid_frame = tk.Frame(app, bg=THEME["bg"])
    mid_frame.pack(pady=(20, 0))

    lbl_temp = tk.Label(mid_frame, text="🌤", font=("Segoe UI Light", 72), bg=THEME["bg"], fg=THEME["fg"])
    lbl_temp.pack()

    lbl_desc = tk.Label(mid_frame, text="Welcome", font=("Segoe UI", 18), bg=THEME["bg"], fg=THEME["fg"])
    lbl_desc.pack(pady=(0, 10))

    lbl_loc = tk.Label(mid_frame, text="Enter a city above", font=("Segoe UI", 14), bg=THEME["bg"], fg=THEME["sub"])
    lbl_loc.pack(pady=(0, 20))

    lbl_stats = tk.Label(mid_frame, text="", font=("Segoe UI", 12), bg=THEME["bg"], fg=THEME["sub"])
    lbl_stats.pack()

    app.mainloop()