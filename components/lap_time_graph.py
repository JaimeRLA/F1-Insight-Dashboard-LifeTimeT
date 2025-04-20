import plotly.graph_objs as go
from utils.helpers import format_lap_time

def generate_lap_time_figure(raw_data, driver_number=55):
    lap_numbers = []
    lap_times = []
    formatted_times = []

    for lap in raw_data:
        if lap.get("driver_number") == driver_number and lap.get("lap_duration") is not None:
            lap_number = lap["lap_number"]
            duration = lap["lap_duration"]
            lap_numbers.append(lap_number)
            lap_times.append(duration)
            formatted_times.append(format_lap_time(duration))

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
            title=f'Lap Times vs. Lap Number (Driver {driver_number})',
            xaxis=dict(title='Lap Number', color='white', gridcolor='#444'),
            yaxis=dict(title='Lap Duration (seconds)', color='white', gridcolor='#444'),
            hovermode='closest'
        )
    }
