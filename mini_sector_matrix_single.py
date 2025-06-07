import plotly.graph_objs as go

# Color scale: normalized values from 0 to 1
color_scale = [
    [0.00, '#222222'],  # None
    [0.25, '#FFFF00'],  # 2048 - Yellow
    [0.50, '#00FF00'],  # 2049 - Green
    [0.75, '#8000FF'],  # 2051 - Purple
    [1.00, '#FF69B4']   # 2064 - Pink
]

# Map raw segment codes to scale indices
segment_code_map = {
    None: 0,
    2048: 1,
    2049: 2,
    2051: 3,
    2064: 4
}

def generate_mini_sector_heatmap(raw_data):
    if not raw_data:
        return {'data': [], 'layout': go.Layout(title='No Data')}

    # Get the latest lap for each driver
    latest_laps = {}
    for lap in raw_data:
        driver = lap.get("driver_number")
        lap_num = lap.get("lap_number", 0)
        if driver not in latest_laps or lap_num > latest_laps[driver].get("lap_number", 0):
            latest_laps[driver] = lap

    z = []
    y_labels = []
    max_segments = 0

    for driver, lap in sorted(latest_laps.items()):
        segments = (
            lap.get('segments_sector_1', []) +
            lap.get('segments_sector_2', []) +
            lap.get('segments_sector_3', [])
        )
        max_segments = max(max_segments, len(segments))

        z_row = [segment_code_map.get(code, 0) for code in segments]
        z.append(z_row)
        y_labels.append(f"Driver {driver}")  # ✅ Removed lap number

    for row in z:
        row += [0] * (max_segments - len(row))

    trace = go.Heatmap(
        z=z,
        x=[f"S{i+1}" for i in range(max_segments)],
        y=y_labels,
        hoverinfo='skip',
        colorscale=color_scale,
        zmin=0,
        zmax=4,
        showscale=False,
        xgap=1,
        ygap=1
    )

    return {
        'data': [trace],
        'layout': go.Layout(
            title="Mini Sector Breakdown - Last Lap per Driver",
            paper_bgcolor='#111111',
            plot_bgcolor='#111111',
            font=dict(color='white'),
            xaxis=dict(tickfont=dict(color='white'), side='top'),
            margin=dict(t=60, l=80, r=40, b=60),
            height=max(200, 30 * len(y_labels))
        )
    }
