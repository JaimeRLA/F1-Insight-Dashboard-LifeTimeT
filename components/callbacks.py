# callbacks.py

from dash import Input, Output
from app import app

from utils.fetch_data import (
    fetch_lap_data,
    fetch_stint_data,
    fetch_weather_data,
    fetch_position_data,
    fetch_meeting_data,
    fetch_pit_data,
    fetch_message_data
)

from top_speed_line import generate_top_speed_plot
from lap_time_graph import generate_lap_time_figure
from mini_sector_matrix import generate_mini_sector_heatmap
from sector_time_hm import generate_sector_time_heatmap
from stint_visualization import generate_stint_visualization
from live_message_box import get_latest_message
from last_pitstop_box import get_last_pitstop_box
from meeting_info_box import display_meeting_info
from weather_box import render_weather_box
from driver_position_box import render_driver_position_line

# Número del piloto que estás siguiendo
driver_number = 16

# === 1. Callbacks para cargar datos a los Stores (1 llamada por tipo de dato) ===

@app.callback(Output('lap-data-store', 'data'), Input('live-update-interval', 'n_intervals'))
def update_lap_store(n):
    return fetch_lap_data()

@app.callback(Output('stint-data-store', 'data'), Input('live-update-interval', 'n_intervals'))
def update_stint_store(n):
    return fetch_stint_data()

@app.callback(Output('weather-data-store', 'data'), Input('live-update-interval', 'n_intervals'))
def update_weather_store(n):
    return fetch_weather_data()

@app.callback(Output('position-data-store', 'data'), Input('live-update-interval', 'n_intervals'))
def update_position_store(n):
    return fetch_position_data()

@app.callback(Output('meeting-data-store', 'data'), Input('live-update-interval', 'n_intervals'))
def update_meeting_store(n):
    return fetch_meeting_data()

@app.callback(Output('pit-data-store', 'data'), Input('live-update-interval', 'n_intervals'))
def update_pit_store(n):
    return fetch_pit_data()

@app.callback(Output('message-data-store', 'data'), Input('live-update-interval', 'n_intervals'))
def update_message_store(n):
    return fetch_message_data()


# === 2. Callbacks para actualizar gráficos usando datos desde Store ===

@app.callback(Output('top-speed-graph', 'figure'), Input('lap-data-store', 'data'))
def update_top_speed(data):
    return generate_top_speed_plot(data, driver_number)

@app.callback(Output('lap-time-graph', 'figure'), Input('lap-data-store', 'data'))
def update_lap_times(data):
    return generate_lap_time_figure(data, driver_number)

@app.callback(Output('mini-sector-matrix', 'figure'), Input('lap-data-store', 'data'))
def update_sector_matrix(data):
    return generate_mini_sector_heatmap(data, driver_number)

@app.callback(Output('sector-time-heatmap', 'figure'), Input('lap-data-store', 'data'))
def update_sector_heatmap(data):
    return generate_sector_time_heatmap(data, target_driver=driver_number)

@app.callback(Output('stint-visualization', 'figure'), Input('stint-data-store', 'data'))
def update_stint_graph(data):
    return generate_stint_visualization(data, driver_number)


# === 3. Callbacks para actualizar cajas de información ===

@app.callback(Output('latest-message-box', 'children'), Input('message-data-store', 'data'))
def update_message(data):
    return get_latest_message(data)

@app.callback(Output('last-pitstop-box', 'children'), Input('pit-data-store', 'data'))
def update_pit_box(data):
    return get_last_pitstop_box(data, driver_number)

@app.callback(Output('meeting-info-box', 'children'), Input('meeting-data-store', 'data'))
def update_meeting_box(data):
    return display_meeting_info(data)

@app.callback(Output('weather-box', 'children'), Input('weather-data-store', 'data'))
def update_weather(data):
    return render_weather_box(data)

@app.callback(Output('position-box', 'children'), Input('position-data-store', 'data'))
def update_position(data):
    return render_driver_position_line(data, driver_number)
