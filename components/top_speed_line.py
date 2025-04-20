import plotly.graph_objs as go

def generate_top_speed_plot(raw_data, driver_number=55):
    # Validación y filtrado de datos del piloto
    try:
        valid_laps = [
            lap for lap in raw_data
            if str(lap.get("driver_number")) == str(driver_number)
            and lap.get("lap_number") is not None
            and lap.get("st_speed") is not None
        ]
    except Exception as e:
        print(f"[TopSpeed] Error filtrando datos: {e}")
        return {'data': [], 'layout': go.Layout(title='Error de datos')}

    if not valid_laps:
        return {
            'data': [],
            'layout': go.Layout(
                title=f"Sin datos de velocidad para el piloto {driver_number}",
                paper_bgcolor='#111111',
                plot_bgcolor='#111111',
                font=dict(color='white')
            )
        }

    # Ordenar por número de vuelta
    valid_laps.sort(key=lambda x: x['lap_number'])

    lap_numbers = [lap['lap_number'] for lap in valid_laps]
    st_speeds = [lap['st_speed'] for lap in valid_laps]

    trace = go.Scatter(
        x=lap_numbers,
        y=st_speeds,
        mode='lines+markers',
        name=f'Driver {driver_number}',
        line=dict(color='#00BFFF', width=3),
        marker=dict(color='white', size=6),
        hovertemplate="Lap %{x}<br>Top Speed: %{y} km/h<extra></extra>"
    )

    layout = go.Layout(
        title=f"Top Speed por vuelta (Piloto {driver_number})",
        paper_bgcolor='#111111',
        plot_bgcolor='#111111',
        font=dict(color='white'),
        xaxis=dict(title='Número de Vuelta', tickfont=dict(color='white'), gridcolor='#444'),
        yaxis=dict(title='Velocidad Máxima (km/h)', tickfont=dict(color='white'), gridcolor='#444'),
        margin=dict(t=50, l=60, r=40, b=60),
        hovermode='closest',
        transition={'duration': 500}
    )

    return {'data': [trace], 'layout': layout}
