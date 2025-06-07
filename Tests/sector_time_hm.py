import plotly.graph_objs as go

def generate_sector_time_heatmap(all_data, target_driver=55):
    driver_laps = sorted(
        [lap for lap in all_data if lap.get("driver_number") == target_driver],
        key=lambda x: x["lap_number"]
    )
    if not driver_laps:
        return {'data': [], 'layout': go.Layout(title='No Data')}

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

    best_so_far = {"sector_1": float('inf'), "sector_2": float('inf'), "sector_3": float('inf')}

    z, text = [], []

    for lap in driver_laps:
        row = []
        text_row = []
        lap_num = lap['lap_number']

        # Warm-up lap logic (mark all sectors orange)
        if lap.get("duration_sector_1") is None:
            for i in range(3):
                row.append(4)  # Orange value
                text_row.append(f"Lap {lap_num} - Sector {i+1}<br><b>Warm-up lap</b>")
            z.append(row)
            text.append(text_row)
            continue

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
                row.append(3)
                text_row.append(f"{lap_label}<br><b>Session Best</b>: {val:.3f}s")
            elif val < best_so_far[sector]:
                best_so_far[sector] = val
                row.append(2)
                text_row.append(f"{lap_label}<br><b>Personal Improvement</b>: {val:.3f}s")
            else:
                row.append(1)
                text_row.append(f"{lap_label}<br>{val:.3f}s")

        z.append(row)
        text.append(text_row)

    color_scale = [
        [0.00, '#222222'],  # No data
        [0.25, '#FFFF00'],  # Yellow
        [0.50, '#00FF00'],  # Green
        [0.75, '#8000FF'],  # Purple
        [1.00, '#FFA500']   # Orange (warm-up)
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
        zmax=4,
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
