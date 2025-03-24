import plotly.graph_objs as go
from utils.helpers import format_lap_time

def generate_lap_time_figure(lap_data):
    lap_numbers = []
    lap_times = []
    formatted_times = []

    for lap, time in lap_data.items():
        if time is not None:
            lap_numbers.append(lap)
            lap_times.append(time)
            formatted_times.append(format_lap_time(time))


    return {
        'data': [
            go.Scatter(
                x=lap_numbers,
                y=lap_times,
                mode='lines+markers',
                line=dict(color='#E50914', width=3),
                marker=dict(size=8, color='white'),
                name='Lap Duration',
                customdata=list(zip(lap_numbers, formatted_times)),
                hovertemplate="<b>Lap %{customdata[0]}</b><br>Time: %{customdata[1]}<extra></extra>"
            )
        ],
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
