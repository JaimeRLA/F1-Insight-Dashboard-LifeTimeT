import plotly.graph_objs as go

color_map = {
    2048: '#FFFF00',
    2049: '#00FF00',
    2051: '#8000FF',
    None: '#FF00FF'
}

def generate_mini_sector_figure(lap_sector_data):
    traces = []
    for lap in lap_sector_data:
        lap_label = f"Lap {lap['lap_number']}"
        segments = lap['segments_sector_1'] + lap['segments_sector_2'] + lap['segments_sector_3']
        for col_index, seg in enumerate(segments):
            traces.append(
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

    return {
        'data': traces,
        'layout': go.Layout(
            title='Mini-Sector Performance Grid',
            barmode='stack',
            paper_bgcolor='#111111',
            plot_bgcolor='#111111',
            font=dict(color='white'),
            xaxis=dict(title='Mini-Sector Index', showgrid=False, tickfont=dict(color='white')),
            yaxis=dict(title='Lap', showgrid=False, tickfont=dict(color='white')),
            height=20 * len(lap_sector_data),
            margin=dict(t=50, l=20, r=20, b=60)
        )
    }
