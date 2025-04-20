import plotly.graph_objs as go

def generate_sector_time_heatmap(all_data, target_driver=55):
    # Filtrar vueltas del piloto objetivo
    driver_laps = sorted(
        [lap for lap in all_data if lap.get("driver_number") == target_driver],
        key=lambda x: x["lap_number"]
    )
    if not driver_laps:
        return {'data': [], 'layout': go.Layout(title='No Data')}

    # Organizar datos por lap_number para cada sector
    sector_data_by_lap = {
        "sector_1": {},
        "sector_2": {},
        "sector_3": {}
    }

    for lap in all_data:
        lap_num = lap.get("lap_number")
        for sector in ["sector_1", "sector_2", "sector_3"]:
            val = lap.get(f"duration_{sector}")
            if lap_num is not None and val is not None:
                sector_data_by_lap[sector].setdefault(lap_num, []).append(val)

    # Inicializar best_so_far para mejoras personales
    best_so_far = {"sector_1": float('inf'), "sector_2": float('inf'), "sector_3": float('inf')}

    z, text = [], []

    for lap in driver_laps:
        row = []
        text_row = []
        lap_num = lap['lap_number']

        for i, sector in enumerate(["sector_1", "sector_2", "sector_3"]):
            val = lap.get(f"duration_{sector}")
            lap_label = f"Lap {lap_num} - Sector {i+1}"

            if val is None:
                row.append(0)
                text_row.append(f"{lap_label}<br>No data")
                continue

            sector_times_this_lap = sector_data_by_lap[sector].get(lap_num, [])
            min_sector_time = min(sector_times_this_lap) if sector_times_this_lap else float('inf')

            if val <= min_sector_time:
                row.append(3)  # Púrpura (el mejor de todos en ese sector de esa vuelta)
                text_row.append(f"{lap_label}<br><b>Session Best</b>: {val:.3f}s")
            elif val < best_so_far[sector]:
                best_so_far[sector] = val
                row.append(2)  # Verde (mejora personal)
                text_row.append(f"{lap_label}<br><b>Personal Improvement</b>: {val:.3f}s")
            else:
                row.append(1)  # Amarillo (sin mejora)
                text_row.append(f"{lap_label}<br>{val:.3f}s")

        z.append(row)
        text.append(text_row)

    color_scale = [
        [0.00, '#222222'],  # Sin datos
        [0.33, '#FFFF00'],  # Amarillo (sin mejora)
        [0.66, '#00FF00'],  # Verde (mejora personal)
        [1.00, '#8000FF'],  # Púrpura (mejor de la sesión)
    ]

    trace = go.Heatmap(
        z=z,
        x=["Sector 1", "Sector 2", "Sector 3"],
        y=[f"Lap {lap['lap_number']}" for lap in driver_laps],
        text=text,
        texttemplate="%{text}",
        hoverinfo='text',
        colorscale=color_scale,
        zmin=0,
        zmax=3,
        showscale=False,
        xgap=1,
        ygap=1
    )

    return {
        'data': [trace],
        'layout': go.Layout(
            title=f"Driver {target_driver} Sector Time Progression",
            paper_bgcolor='#111111',
            plot_bgcolor='#111111',
            font=dict(color='white'),
            xaxis=dict(tickfont=dict(color='white'), side='top'),
            yaxis=dict(title="Lap", tickfont=dict(color='white'), autorange="reversed"),
            margin=dict(t=60, l=80, r=40, b=60),
            height=max(200, 30 * len(driver_laps)),
        )
    }
