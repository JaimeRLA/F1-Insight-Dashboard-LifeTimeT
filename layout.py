from dash import html, dcc
from components.lap_time_graph import generate_lap_time_figure
from components.mini_sector_matrix import generate_mini_sector_figure
from utils.fetch_data import fetch_lap_data, fetch_sector_data
from utils.helpers import format_lap_time

def get_layout():
    data = fetch_lap_data()
    sector_data = fetch_sector_data(data)
    lap_data = {lap['lap_number']: lap['lap_duration'] for lap in data if 'lap_duration' in lap}

    return html.Div(
        style={'backgroundColor': '#111111', 'padding': '20px', 'fontFamily': 'Arial'},
        children=[
            html.H1("F1 Lap Dashboard", style={'color': 'white', 'textAlign': 'center'}),

            html.Div([
                dcc.Graph(id='lap-time-graph', figure=generate_lap_time_figure(lap_data))
            ], style={'marginBottom': '50px'}),

            html.Div([
                dcc.Graph(id='mini-sector-matrix', figure=generate_mini_sector_figure(sector_data))
            ])
        ]
    )
