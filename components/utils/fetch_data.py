from urllib.request import urlopen
import json

# utils/fetch_data.py

from urllib.request import urlopen
import json

def fetch_lap_data():
    url = 'https://api.openf1.org/v1/laps?session_key=latest'
    try:
        response = urlopen(url)
        raw = response.read().decode('utf-8')
        data = json.loads(raw)
        print(f"✅ API respondió con {len(data)} vueltas")
        print(data)
        return data
    except Exception as e:
        print(f"❌ Error al hacer fetch desde la API: {e}")
        return []


def fetch_stint_data():
    response = urlopen('https://api.openf1.org/v1/stints?session_key=latest')
    data = json.loads(response.read().decode('utf-8'))
    return data

def fetch_message_data():
    response = urlopen('https://api.openf1.org/v1/race_control?session_key=latest')
    data = json.loads(response.read().decode('utf-8'))
    return data

def fetch_pit_data():
    response = urlopen('https://api.openf1.org/v1/pit?session_key=latest')
    data = json.loads(response.read().decode('utf-8'))
    return data

def fetch_meeting_data():
    response = urlopen('https://api.openf1.org/v1/meetings?meeting_key=latest')
    data = json.loads(response.read().decode('utf-8'))
    return data

def fetch_weather_data():
    response = urlopen('https://api.openf1.org/v1/weather?meeting_key=latest')
    data = json.loads(response.read().decode('utf-8'))
    return data

def fetch_position_data():
    response = urlopen('https://api.openf1.org/v1/position?meeting_key=latest')
    data = json.loads(response.read().decode('utf-8'))
    return data


# === Fetch and Save ===
print("✅ sector_data guardado en sector_data.json")
