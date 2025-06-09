import plotly.graph_objs as go

# Color scale for mini sectors
color_scale = [
    [0.00, '#222222'],
    [0.25, '#FFFF00'],
    [0.50, '#00FF00'],
    [0.75, '#8000FF'],
    [1.00, '#FF69B4']
]

# Segment code to index
segment_code_map = {
    None: 0,
    2048: 1,
    2049: 2,
    2051: 3,
    2064: 4
}

# Team & driver mappings
driver_team_map = {
    4: 'McLaren', 81: 'McLaren',
    1: 'Red Bull', 22: 'Red Bull',
    16: 'Ferrari', 44: 'Ferrari',
    63: 'Mercedes', 12: 'Mercedes',
    5: 'Sauber', 27: 'Sauber',
    31: 'Haas', 87: 'Haas',
    30: 'RB', 6: 'RB',
    55: 'Williams', 23: 'Williams',
    10: 'Alpine', 43: 'Alpine',
    14: 'Aston', 18: 'Aston'
}

team_color_map = {
    'McLaren': '#FF8000',
    'Red Bull': "#00225E",
    'Ferrari': '#DC0000',
    'Mercedes': '#00D2BE',
    'Sauber': '#00E701',
    'Haas': '#B6BABD',
    'RB': '#FFFFFF',
    'Williams': "#266BEC",
    'Alpine': '#FF87BC',
    'Aston': '#00665E'
}


def generate_mini_sector_heatmap(raw_data):
    if not raw_data:
        return {'data': [], 'layout': go.Layout(title='No Data')}

    # Get latest lap per driver
    latest_laps = {}
    for lap in raw_data:
        driver = lap.get("driver_number")
        lap_num = lap.get("lap_number", 0)
        if driver not in latest_laps or lap_num > latest_laps[driver].get("lap_number", 0):
            latest_laps[driver] = lap

    # Sort by team for visual consistency
    sorted_laps = sorted(latest_laps.items(), key=lambda x: driver_team_map.get(x[0], ''))

    z = []
    annotations = []
    y_ticks = []

    max_segments = 0

    for i, (driver, lap) in enumerate(sorted_laps):
        segments = (
            lap.get('segments_sector_1', []) +
            lap.get('segments_sector_2', []) +
            lap.get('segments_sector_3', [])
        )
        z_row = [segment_code_map.get(code, 0) for code in segments]
        z.append(z_row)
        max_segments = max(max_segments, len(z_row))

        # Team label
        team = driver_team_map.get(driver, 'Unknown')
        team_color = team_color_map.get(team, '#FFFFFF')
        annotations.append(dict(
            xref='paper',
            yref='y',
            x=-0.01,  # <-- closer to heatmap
            y=i,
            text=f"Driver {driver}",
            font=dict(color=team_color, size=13),
            showarrow=False,
            xanchor='right'
        ))

        y_ticks.append(i)

    # Pad all rows to match max length
    for row in z:
        row += [0] * (max_segments - len(row))

    trace = go.Heatmap(
        z=z,
        x=[f"MS{i+1}" for i in range(max_segments)],
        y=y_ticks,
        hoverinfo='skip',
        colorscale=color_scale,
        zmin=0,
        zmax=4,
        showscale=False,
        xgap=1,
        ygap=1
    )

    layout = go.Layout(
        title=dict(
            text=" Mini Sector Breakdown – Last Lap per Driver",
            x=0.5,
            font=dict(color='white', size=20)
        ),
        paper_bgcolor='#1a1a1a',
        plot_bgcolor='#111111',
        font=dict(color='white'),
        xaxis=dict(
            tickfont=dict(color='white'),
            side='top',
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            tickvals=y_ticks,
            ticktext=[""] * len(y_ticks),  # Hide default labels
            showgrid=False,
            zeroline=False
        ),
        margin=dict(t=80, l=120, r=40, b=40),
        height=max(300, 30 * len(y_ticks)),
        annotations=annotations
    )

    return {'data': [trace], 'layout': layout}
