import tkinter as tk
from tkinter import messagebox
import requests

# API Endpoints
GEO_API = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API = "https://api.open-meteo.com/v1/forecast"

COLORS = {
    "bg": "#2c2f33",
    "fg": "#ffffff",
    "accent": "#7289da",
    "sub": "#99aab5",
    "input": "#23272a"
}

def get_weather_icon(code):
    if code == 0: return "☀️", "Clear Sky"
    if code <= 3: return "⛅", "Partly Cloudy"
    if code in [45, 48]: return "🌫", "Foggy"
    if code in [51, 53, 55, 61, 63, 65]: return "🌧", "Rain"
    if code in [71, 73, 75, 77]: return "❄️", "Snow"
    if code >= 95: return "⛈", "Thunderstorm"
    return "🌥", "Overcast"

def fetch_weather(city):
    if not city:
        return None, "Please enter a city name."

    try:
        # Get coordinates
        geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}
        geo_res = requests.get(GEO_API, params=geo_params)
        geo_data = geo_res.json()

        if "results" not in geo_data:
            return None, "City not found."

        loc = geo_data["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        
        # Get weather details
        w_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "temperature_unit": "celsius",
            "windspeed_unit": "ms"
        }
        weather_res = requests.get(WEATHER_API, params=w_params)
        data = weather_res.json()

        if "current_weather" in data:
            current = data["current_weather"]
            return {
                "temp": current["temperature"],
                "wind": current["windspeed"],
                "code": current["weathercode"],
                "city": loc["name"],
                "country": loc.get("country_code", "").upper()
            }, None
        
        return None, "Weather data unavailable."

    except Exception as e:
        return None, f"Error: {e}"

def search_command(event=None):
    city_name = entry.get()
    
    btn.config(state=tk.DISABLED)
    data, error = fetch_weather(city_name)
    btn.config(state=tk.NORMAL)

    if error:
        messagebox.showerror("Error", error)
    else:
        icon_symbol, status_text = get_weather_icon(data["code"])
        
        # Updating the labels
        lbl_icon.config(text=icon_symbol)
        lbl_temp.config(text=f"{data['temp']:.0f}°")
        lbl_desc.config(text=status_text)
        lbl_loc.config(text=f"{data['city']}, {data['country']}")
        lbl_wind.config(text=f"Wind: {data['wind']} m/s")

# Setup Main Window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Atmosphere")
    root.geometry("350x500")
    root.resizable(False, False)
    root.configure(bg=COLORS["bg"])

    # Search Area
    frame_top = tk.Frame(root, bg=COLORS["bg"], pady=30)
    frame_top.pack()

    entry = tk.Entry(
        frame_top, font=("Segoe UI", 14), width=18, bd=0, 
        bg=COLORS["input"], fg=COLORS["fg"], 
        insertbackground=COLORS["accent"], justify='center'
    )
    entry.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
    entry.focus()
    entry.bind('<Return>', search_command)

    btn = tk.Button(
        frame_top, text="Go", font=("Segoe UI", 12, "bold"), 
        bg=COLORS["accent"], fg=COLORS["fg"], 
        activebackground=COLORS["accent"], activeforeground=COLORS["fg"],
        command=search_command, relief=tk.FLAT, bd=0, padx=15, pady=2
    )
    btn.pack(side=tk.LEFT)

    # Content Area
    frame_mid = tk.Frame(root, bg=COLORS["bg"])
    frame_mid.pack(pady=(10, 0), padx=20, fill='x')

    # Row for Icon and Temp to ensure alignment
    row_weather = tk.Frame(frame_mid, bg=COLORS["bg"])
    row_weather.pack(pady=10)

    lbl_icon = tk.Label(row_weather, text="🌤", font=("Segoe UI Emoji", 50), bg=COLORS["bg"], fg=COLORS["fg"])
    lbl_icon.pack(side=tk.LEFT, padx=(0, 15))

    lbl_temp = tk.Label(row_weather, text="--°", font=("Segoe UI Light", 50), bg=COLORS["bg"], fg=COLORS["fg"])
    lbl_temp.pack(side=tk.LEFT)

    lbl_desc = tk.Label(frame_mid, text="Welcome", font=("Segoe UI", 16), bg=COLORS["bg"], fg=COLORS["fg"])
    lbl_desc.pack(pady=(10, 5))

    lbl_loc = tk.Label(frame_mid, text="Enter a city above", font=("Segoe UI", 12), bg=COLORS["bg"], fg=COLORS["sub"])
    lbl_loc.pack(pady=(0, 20))

    lbl_wind = tk.Label(frame_mid, text="", font=("Segoe UI", 11), bg=COLORS["bg"], fg=COLORS["sub"])
    lbl_wind.pack(side=tk.BOTTOM, pady=10)

    root.mainloop()