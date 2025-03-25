from urllib.request import urlopen
import json

def fetch_lap_data(driver_number=55):
    url = f"https://api.openf1.org/v1/laps?session_key=latest&driver_number={driver_number}"
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    filtered = [lap for lap in data if lap['lap_number'] in [3,4,5]]
    return filtered


# === Fetch and Save ===
raw_data = fetch_lap_data()


with open("raw_data.json", "w") as f:
    json.dump(raw_data, f, indent=2)

print("✅ sector_data guardado en sector_data.json")
