import plotly.graph_objs as go

def generate_top_speed_plot(raw_data):
    # Filter valid laps with st_speed and lap_number
    valid_laps = [lap for lap in raw_data if lap.get("lap_number") is not None and lap.get("st_speed") is not None]

    if not valid_laps:
        return {'data': [], 'layout': go.Layout(title='No Top Speed Data')}

    lap_numbers = [lap['lap_number'] for lap in valid_laps]
    st_speeds = [lap['st_speed'] for lap in valid_laps]

    trace = go.Scatter(
        x=lap_numbers,
        y=st_speeds,
        mode='lines+markers',
        name='Top Speed',
        line=dict(color='#00BFFF', width=3),
        marker=dict(color='white', size=8),
        hovertemplate="Lap %{x}<br>Top Speed: %{y} km/h<extra></extra>"
    )

    return {
        'data': [trace],
        'layout': go.Layout(
            title="Top Speed per Lap",
            paper_bgcolor='#111111',
            plot_bgcolor='#111111',
            font=dict(color='white'),
            xaxis=dict(title='Lap Number', tickfont=dict(color='white'), gridcolor='#444'),
            yaxis=dict(title='Top Speed (km/h)', tickfont=dict(color='white'), gridcolor='#444'),
            margin=dict(t=50, l=60, r=40, b=60),
            hovermode='closest'
        )
    }
