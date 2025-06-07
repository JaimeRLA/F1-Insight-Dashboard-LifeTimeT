# callbacks.py

from dash import Input, Output
from app import app
from dash import html
import pandas as pd

from utils.fetch_data import (
    fetch_lap_data,
    fetch_stint_data,
    fetch_weather_data,
    fetch_position_data,
    fetch_meeting_data,
    fetch_pit_data,
    fetch_message_data
)

from mini_sector_matrix_single import generate_mini_sector_heatmap
from stint_visualization import generate_stint_visualization
from live_message_box import get_latest_message
from meeting_info_box import display_meeting_info
from weather_box import render_weather_box
from driver_position_box import render_driver_position_box
from sector_split_matrix import generate_sector_split_matrix
from qualifying_classification import (
    classify_sessions,
    build_live_qualifying_result,
    render_qualifying_table
)

# Número del piloto que estás siguiendo
driver_number = 4

# === 1. Callbacks para cargar datos a los Stores ===

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


# === 2. Callbacks para actualizar gráficos y componentes ===

@app.callback(Output('mini-sector-matrix', 'figure'), Input('lap-data-store', 'data'))
def update_mini_sector_matrix(data):
    return generate_mini_sector_heatmap(data)

@app.callback(Output('sector-split-matrix', 'children'), Input('lap-data-store', 'data'))
def update_sector_split_matrix(data):
    return generate_sector_split_matrix(data)

@app.callback(Output('stint-visualization', 'figure'), Input('stint-data-store', 'data'))
def update_stint_graph(data):
    return generate_stint_visualization(data, driver_number)

@app.callback(
    Output('qualifying-classification-box', 'children'),
    [Input('lap-data-store', 'data'), Input('message-data-store', 'data')]
)
def update_qualifying_table(lap_data, message_data):
    df, current_phase = classify_sessions(lap_data, message_data)
    result_df = build_live_qualifying_result(df, current_phase)
    return render_qualifying_table(result_df)



# === 3. Callbacks para actualizar cajas de información ===

@app.callback(Output('latest-message-box', 'children'), Input('message-data-store', 'data'))
def update_message(data):
    return get_latest_message(data)

@app.callback(Output('meeting-info-box', 'children'), Input('meeting-data-store', 'data'))
def update_meeting_box(data):
    return display_meeting_info(data)

@app.callback(Output('weather-box', 'children'), Input('weather-data-store', 'data'))
def update_weather(data):
    return render_weather_box(data)

@app.callback(Output('position-box', 'children'), Input('position-data-store', 'data'))
def update_position(data):
    return render_driver_position_box(data, driver_number)
