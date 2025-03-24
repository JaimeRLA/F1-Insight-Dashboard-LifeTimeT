from urllib.request import urlopen
import json

def fetch_lap_data(driver_number=55):
    url = f"https://api.openf1.org/v1/laps?session_key=latest&driver_number={driver_number}"
    response = urlopen(url)
    return json.loads(response.read().decode('utf-8'))

def fetch_sector_data(data):
    lap_list = []
    for lap in data:
        if all(k in lap for k in ['lap_number', 'segments_sector_1', 'segments_sector_2', 'segments_sector_3']):
            lap_list.append({
                'lap_number': lap['lap_number'],
                'segments_sector_1': lap['segments_sector_1'],
                'segments_sector_2': lap['segments_sector_2'],
                'segments_sector_3': lap['segments_sector_3']
            })
    return lap_list
