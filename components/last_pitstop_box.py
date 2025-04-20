from dash import html
from datetime import datetime

def get_last_pitstop_box(pit_data, driver_number):
    if not pit_data:
        return html.Div("No pit stop data available", style={'color': 'white'})

    # Filter for the selected driver's pit stops
    driver_pits = [pit for pit in pit_data if pit['driver_number'] == driver_number]
    if not driver_pits:
        return html.Div(f"No pit stop data for driver {driver_number}", style={'color': 'white'})

    # Get the latest pit stop by date
    latest_pit = sorted(driver_pits, key=lambda x: x['date'], reverse=True)[0]

    # Format date
    time_str = datetime.fromisoformat(latest_pit['date']).strftime('%Y-%m-%d %H:%M:%S')

    return html.Div([
        html.H4("Last Pit Stop", style={'color': 'white', 'marginBottom': '10px'}),
        html.P(f"Driver: {latest_pit['driver_number']}", style={'color': 'white'}),
        html.P(f"Lap: {latest_pit['lap_number']}", style={'color': 'white'}),
        html.P(f"Duration: {latest_pit['pit_duration']}s", style={'color': 'white'}),
        html.P(f"Time: {time_str}", style={'color': '#AAAAAA', 'fontSize': '12px'})
    ], style={
        'backgroundColor': '#444',
        'borderRadius': '16px',
        'padding': '60px',
        'boxShadow': '0 4px 10px rgba(0,0,0,0.5)',
        'width': '230px'
    })
