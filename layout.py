from dash import html, dcc
from components.lap_time_graph import generate_lap_time_figure
from components.mini_sector_matrix import generate_mini_sector_heatmap
from components.top_speed_line import generate_top_speed_plot
from utils.fetch_data import fetch_lap_data

def get_layout():
    data = fetch_lap_data()
    lap_data = {lap['lap_number']: lap['lap_duration'] for lap in data if 'lap_duration' in lap and lap['lap_duration'] is not None}

    return html.Div(
    style={'backgroundColor': '#111111', 'padding': '40px', 'fontFamily': 'Arial'},
    children=[
        html.H1("F1 Lap Dashboard", style={'color': 'white', 'textAlign': 'center', 'marginBottom': '40px'}),

        html.Div([
            # Left Column
            html.Div([
                html.Div([
                    html.H3("Lap Times", style={'color': 'white', 'textAlign': 'center'}),
                    dcc.Graph(
                        id='lap-time-graph',
                        figure=generate_lap_time_figure(lap_data),
                        config={'displayModeBar': False}
                    )
                ], style={
                    'backgroundColor': '#333333',
                    'borderRadius': '16px',
                    'padding': '20px',
                    'marginBottom': '20px',
                    'height': '600px',
                    'boxShadow': '0 4px 10px rgba(0,0,0,0.5)'
                }),

                html.Div([
                    html.H3("Top Speed", style={'color': 'white', 'textAlign': 'center'}),
                    dcc.Graph(
                        id='top-speed-graph',
                        figure=generate_top_speed_plot(data),
                        config={'displayModeBar': False}
                    )
                ], style={
                    'backgroundColor': '#333333',
                    'borderRadius': '16px',
                    'padding': '20px',
                    'height': '600px',
                    'boxShadow': '0 4px 10px rgba(0,0,0,0.5)'
                }),
            ], style={'flex': '1', 'marginRight': '20px'}),

            # Right Column
            html.Div([
                html.H3("Mini-Sector Matrix", style={'color': 'white', 'textAlign': 'center'}),
                dcc.Graph(
                    id='mini-sector-matrix',
                    figure=generate_mini_sector_heatmap(data),
                    config={'displayModeBar': False}
                )
            ], style={
                'backgroundColor': '#333333',
                'borderRadius': '16px',
                'padding': '20px',
                'flex': '1',
                'height': '1800px',
                'boxShadow': '0 4px 10px rgba(0,0,0,0.5)'
            })
        ], style={'display': 'flex', 'flexDirection': 'row'})
    ]
)
