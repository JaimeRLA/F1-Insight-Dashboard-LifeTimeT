import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import requests
from geopy.geocoders import Nominatim

# Replace with your OpenWeatherMap API key
OPENWEATHER_API_KEY = 'ba263655f5732e0bbf951581411302c7'


app = dash.Dash(__name__)

# Default location
DEFAULT_LOCATION = "London"
geolocator = Nominatim(user_agent="weather_map")
location = geolocator.geocode(DEFAULT_LOCATION)
default_lat, default_lon = location.latitude, location.longitude

def get_forecast(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast?"
        f"lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    resp = requests.get(url)
    data = resp.json()
    print(data)  # <-- Add this line
    return data

def extract_rain_data(forecast_data):
    times = []
    lats = []
    lons = []
    rains = []
    for entry in forecast_data['list']:
        rain = entry.get('rain', {}).get('3h', 0)
        times.append(entry['dt_txt'])
        lats.append(forecast_data['city']['coord']['lat'])
        lons.append(forecast_data['city']['coord']['lon'])
        rains.append(rain)
    return times, lats, lons, rains

# Initial data
forecast_data = get_forecast(default_lat, default_lon)
times, lats, lons, rains = extract_rain_data(forecast_data)

app.layout = html.Div([
    html.H1("Weather Map Forecast"),
    html.Div([
        dcc.Input(id='location-input', type='text', value=DEFAULT_LOCATION, placeholder='Enter location'),
        html.Button('Go', id='go-button', n_clicks=0)
    ]),
    dcc.Slider(
        id='time-slider',
        min=0,
        max=len(times)-1,
        value=0,
        marks={i: times[i][:16] for i in range(0, len(times), max(1, len(times)//5))},
        step=1
    ),
    dcc.Graph(id='weather-map')
])

@app.callback(
    Output('weather-map', 'figure'),
    Output('time-slider', 'max'),
    Output('time-slider', 'marks'),
    Input('time-slider', 'value'),
    Input('go-button', 'n_clicks'),
    State('location-input', 'value')
)
def update_map(selected_time_idx, n_clicks, location_name):
    # Geocode location
    loc = geolocator.geocode(location_name)
    if not loc:
        loc = geolocator.geocode(DEFAULT_LOCATION)
    lat, lon = loc.latitude, loc.longitude

    # Get forecast
    forecast_data = get_forecast(lat, lon)
    times, lats, lons, rains = extract_rain_data(forecast_data)

    # Prepare map
    rain = rains[selected_time_idx]
    time = times[selected_time_idx]
    fig = go.Figure(go.Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=20,
            color=rain,
            colorscale='Blues',
            cmin=0,
            cmax=max(rains) if max(rains) > 0 else 1,
            showscale=True,
            colorbar=dict(title="Rain (mm)")
        ),
        text=[f"Rain: {rain} mm<br>Time: {time}"],
        hoverinfo='text'
    ))
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": lat, "lon": lon},
        mapbox_zoom=7,
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    marks = {i: times[i][:16] for i in range(0, len(times), max(1, len(times)//5))}
    return fig, len(times)-1, marks

if __name__ == '__main__':
    app.run_server(debug=True)