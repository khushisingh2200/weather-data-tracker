import requests
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

CSV_FILE = "weather_data.csv"

def save_to_csv(city, country, temperature, windspeed, winddirection, is_day):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = {
        "timestamp":     timestamp,
        "city":          city,
        "country":       country,
        "temperature":   temperature,
        "windspeed":     windspeed,
        "winddirection": winddirection,
        "is_day":        "yes" if is_day else "no"
    }
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])
    df.to_csv(CSV_FILE, index=False)
    print(f"Data saved to {CSV_FILE}")

def analyse_data():
    if not os.path.exists(CSV_FILE):
        print("No data yet — run the weather tracker first")
        return
    df = pd.read_csv(CSV_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    print("\n--- Weather Data Summary ---")
    print(f"Total records: {len(df)}")
    print(f"Cities tracked: {df['city'].unique().tolist()}")
    print(f"Average temperature: {df['temperature'].mean():.1f}C")
    print(f"Max temperature: {df['temperature'].max()}C")
    print(f"Min temperature: {df['temperature'].min()}C")
    print(f"Average wind speed: {df['windspeed'].mean():.1f} mph")

    # ── Chart 1 — Temperature over time ──
    os.makedirs("charts", exist_ok=True)
    plt.figure(figsize=(10, 5))
    for city in df["city"].unique():
        city_df = df[df["city"] == city]
        plt.plot(city_df["timestamp"], city_df["temperature"],
                 marker="o", label=city)
    plt.title("Temperature Over Time by City")
    plt.xlabel("Time")
    plt.ylabel("Temperature (C)")
    plt.xticks(rotation=30, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig("charts/temperature_trend.png")
    plt.show()
    print("Chart saved: charts/temperature_trend.png")

    # ── Chart 2 — Wind speed by city ──
    avg_wind = df.groupby("city")["windspeed"].mean().sort_values(ascending=False)
    plt.figure(figsize=(8, 4))
    plt.bar(avg_wind.index, avg_wind.values, color="steelblue")
    plt.title("Average Wind Speed by City")
    plt.xlabel("City")
    plt.ylabel("Wind Speed (mph)")
    plt.tight_layout()
    plt.savefig("charts/wind_speed_by_city.png")
    plt.show()
    print("Chart saved: charts/wind_speed_by_city.png")

def get_weather():
    while True:
        input_city = input("\nEnter city name (or 'quit' to exit, 'analyse' to see trends): ").strip()

        if input_city.lower() == "quit":
            break

        if input_city.lower() == "analyse":
            analyse_data()
            continue

        params = {"name": input_city, "count": 10}
        try:
            response = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params=params, timeout=5
            )
        except requests.exceptions.ConnectionError:
            print("Connection Error — check your internet")
            continue
        except requests.exceptions.Timeout:
            print("Timeout Error — try again")
            continue

        weather_data = response.json()
        if not weather_data.get("results"):
            print("No results found — check spelling")
            continue

        city      = weather_data["results"][0]["name"]
        country   = weather_data["results"][0]["country"]
        latitude  = weather_data["results"][0]["latitude"]
        longitude = weather_data["results"][0]["longitude"]

        params = {
            "latitude":        latitude,
            "longitude":       longitude,
            "current_weather": True
        }
        response_1     = requests.get("https://api.open-meteo.com/v1/forecast", params=params)
        weather_report = response_1.json()
        current        = weather_report["current_weather"]

        temperature   = current["temperature"]
        windspeed     = current["windspeed"]
        winddirection = current["winddirection"]
        is_day        = current["is_day"]

        print(f"\n{city}, {country}")
        print(f"Temperature:     {temperature} C")
        print(f"Wind Speed:      {windspeed} mph")
        print(f"Wind Direction:  {winddirection} degrees")
        print(f"Daytime:         {'yes' if is_day else 'no'}")

        save_to_csv(city, country, temperature, windspeed, winddirection, is_day)

if __name__ == "__main__":
    print("=== Weather Data Tracker ===")
    print("Track weather for multiple cities and analyse trends over time")
    get_weather()