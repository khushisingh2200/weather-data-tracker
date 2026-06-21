# Weather Data Tracker & Analyser

A Python CLI tool that fetches real-time weather data from a free REST API,
saves it to CSV, and generates trend analysis charts using pandas and matplotlib.

---

## What This Project Does

1. Takes a city name as input
2. Calls the Open-Meteo geocoding API to get coordinates
3. Uses coordinates to fetch current weather data
4. Saves each record to a CSV file with a timestamp
5. Analyses collected data and generates temperature and wind speed charts

---

## Project Structure

    weather-data-tracker/
    ├── main.py
    ├── requirements.txt
    └── README.md

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| requests | REST API calls |
| JSON | Parsing API responses |
| pandas | Data storage and analysis |
| matplotlib | Chart generation |

---

## APIs Used

- Open-Meteo Geocoding API — converts city name to coordinates
- Open-Meteo Forecast API — fetches current weather data
- Both APIs are completely free with no API key required

---

## How to Run

**Step 1 — Install dependencies:**
```bash
pip install -r requirements.txt
```

**Step 2 — Run the tracker:**
```bash
python main.py
```

**Step 3 — Commands:**
- Type any city name to fetch and save weather
- Type `analyse` to generate charts from collected data
- Type `quit` to exit

---

## Features

- Fetches real-time temperature, wind speed, wind direction, and daytime status
- Saves data to CSV with timestamp for trend analysis
- Error handling for connection errors, timeouts, and invalid city names
- Generates temperature trend chart over time per city
- Generates average wind speed comparison chart across cities