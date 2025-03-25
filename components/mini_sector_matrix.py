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

    lap_labels = [f"Lap {lap['lap_number']}" for lap in raw_data]
    max_segments = max(
        len(lap['segments_sector_1'] + lap['segments_sector_2'] + lap['segments_sector_3'])
        for lap in raw_data
    )

    z = []

    for lap in raw_data:
        segments = (
            lap.get('segments_sector_1', []) +
            lap.get('segments_sector_2', []) +
            lap.get('segments_sector_3', [])
        )

        # Pad to align all laps visually
        segments += [None] * (max_segments - len(segments))

        z_row = [segment_code_map.get(code, 0) for code in segments]
        z.append(z_row)

    trace = go.Heatmap(
        z=z,
        x=[f"S{i+1}" for i in range(max_segments)],
        y=lap_labels,
        hoverinfo='skip',  # disables hover info
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
            paper_bgcolor='#111111',
            plot_bgcolor='#111111',
            font=dict(color='white'),
            xaxis=dict(tickfont=dict(color='white'), side='top'),
            yaxis=dict(title="Lap", tickfont=dict(color='white'), autorange="reversed"),
            margin=dict(t=60, l=80, r=40, b=60),
            height=max(200, 30 * len(raw_data)),
        )
    }
