from dash import html

def render_weather_box(weather_data):
    if not weather_data:
        return html.Div("No weather data available", style={'color': 'white'})

    info = weather_data[0]

    return html.Div([
        html.P(f"Air Temp: {info.get('air_temperature')}°C", style={'color': 'white'}),
        html.P(f"Track Temp: {info.get('track_temperature')}°C", style={'color': 'white'}),
        html.P(f"Humidity: {info.get('humidity')}%", style={'color': 'white'}),
        html.P(f"Pressure: {info.get('pressure')} hPa", style={'color': 'white'}),
        html.P(f"Wind: {info.get('wind_speed')} m/s at {info.get('wind_direction')}°", style={'color': 'white'}),
        html.P(f"Rainfall: {info.get('rainfall')} mm", style={'color': 'white'}),
        html.P(f"Updated: {info.get('date')}", style={'color': '#AAAAAA', 'fontSize': '12px'}),
    ], style={
        'backgroundColor': '#444',
        'borderRadius': '12px',
        'padding': '20px',
        'boxShadow': '0 4px 10px rgba(0,0,0,0.5)',
        'width': '300px'
    })
