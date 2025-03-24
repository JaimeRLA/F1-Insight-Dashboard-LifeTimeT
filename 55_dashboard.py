
from urllib.request import urlopen
import json
import dash
from dash import dcc, html
import plotly.graph_objs as go





# ========== LAP TIME DATA ==========

def fetch_live_lap_data(driver_number=55):
    url = f"https://api.openf1.org/v1/laps?session_key=latest&driver_number={driver_number}"
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))

    lap_data = {}
    for lap in data:
        lap_number = lap.get("lap_number")
        lap_duration = lap.get("lap_duration")
        if lap_number and lap_duration:
            lap_data[lap_number] = lap_duration

    return lap_data


lap_data=fetch_live_lap_data(driver_number=55)

def format_lap_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{minutes}:{secs:02d}.{millis:03d}"

lap_numbers = list(lap_data.keys())
lap_times = list(lap_data.values())
formatted_times = [format_lap_time(t) for t in lap_times]

lap_time_trace = go.Scatter(
    x=lap_numbers,
    y=lap_times,
    mode='lines+markers',
    line=dict(color='#E50914', width=3),
    marker=dict(size=8, color='white'),
    name='Lap Duration',
    customdata=list(zip(lap_numbers, formatted_times)),
    hovertemplate="<b>Lap %{customdata[0]}</b><br>Time: %{customdata[1]}<extra></extra>"
)

lap_time_figure = {
    'data': [lap_time_trace],
    'layout': go.Layout(
        paper_bgcolor='#111111',
        plot_bgcolor='#111111',
        font=dict(color='white'),
        title='Lap Times vs. Lap Number',
        xaxis=dict(title='Lap Number', color='white', gridcolor='#444'),
        yaxis=dict(title='Lap Duration (seconds)', color='white', gridcolor='#444'),
        hovermode='closest'
    )
}

# ========== MINI-SECTOR MATRIX DATA ==========
data = [
    {
        'lap_number': 2,
        'segments_sector_1': [2049, 2049, 2049, 2049, 2049, 2048, 2049, 2049, 2048],
        'segments_sector_2': [2049, 2048, 2048, 2049, 2049, 2049],
        'segments_sector_3': [2049, 2048, 2048, 2048, 2049, 2049]
    },
    {
        'lap_number': 3,
        'segments_sector_1': [2049, 2049, 2049, 2049, 2049, 2048, 2049, 2049, 2048],
        'segments_sector_2': [2049, 2049, 2051, 2049, 2049, 2048],
        'segments_sector_3': [2049, 2049, 2049, 2049, 2049, 2048]
    },
    {
        'lap_number': 4,
        'segments_sector_1': [2049, 2049, 2049, 2049, 2049, 2048, 2049, 2049, 2048],
        'segments_sector_2': [2049, 2049, 2051, 2049, 2049, 2048],
        'segments_sector_3': [2049, 2049, 2049, 2049, 2049, 2048]
    },
    {
        'lap_number': 5,
        'segments_sector_1': [2049, 2049, 2049, 2049, 2049, 2048, 2049, 2049, 2048],
        'segments_sector_2': [2049, 2049, 2051, 2049, 2049, 2048],
        'segments_sector_3': []
    }
]

color_map = {
    2048: '#FFFF00',  # Yellow
    2049: '#00FF00',  # Green
    2051: '#8000FF'   # Purple
}

segment_traces = []
for lap in data:
    lap_label = f"Lap {lap['lap_number']}"
    segments = lap['segments_sector_1'] + lap['segments_sector_2'] + lap['segments_sector_3']
    for col_index, seg in enumerate(segments):
        segment_traces.append(
            go.Bar(
                x=[col_index],
                y=[lap_label],
                orientation='h',
                width=1,
                marker=dict(color=color_map.get(seg, 'gray')),
                hovertemplate=f"{lap_label} - Segment {col_index + 1}<br>Code: {seg}<extra></extra>",
                showlegend=False
            )
        )

mini_sector_figure = {
    'data': segment_traces,
    'layout': go.Layout(
        title='Mini-Sector Performance Grid',
        barmode='stack',
        paper_bgcolor='#111111',
        plot_bgcolor='#111111',
        font=dict(color='white'),
        xaxis=dict(title='Mini-Sector Index', showgrid=False, tickfont=dict(color='white')),
        yaxis=dict(title='Lap', showgrid=False, tickfont=dict(color='white')),
        height=80 * len(data),
        margin=dict(t=50, l=60, r=20, b=60)
    )
}

# ========== DASH APP ==========
app = dash.Dash(__name__)
app.title = "F1 Full Dashboard"

app.layout = html.Div(
    style={'backgroundColor': '#111111', 'padding': '20px', 'fontFamily': 'Arial'},
    children=[
        html.H1("F1 Lap Dashboard", style={'color': 'white', 'textAlign': 'center'}),
        
        html.Div([
            dcc.Graph(id='lap-time-graph', figure=lap_time_figure)
        ], style={'marginBottom': '50px'}),

        html.Div([
            dcc.Graph(id='mini-sector-matrix', figure=mini_sector_figure)
        ])
    ]
)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
