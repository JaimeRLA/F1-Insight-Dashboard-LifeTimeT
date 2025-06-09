import plotly.graph_objs as go

# Tyre compound colors
compound_colors = {
    "SOFT": "#FF4C4C",
    "MEDIUM": "#FFD700",
    "HARD": "#FFFFFF",
    "INTERMEDIATE": "#39FF14",
    "WET": "#1E90FF"
}

# Driver to team mapping
driver_team_map = {
    1: 'Red Bull',  4: 'McLaren',  5: 'Sauber',    6: 'RB',       10: 'Alpine',
    12: 'Mercedes', 14: 'Aston',   16: 'Ferrari',  18: 'Aston',   20: 'Haas',
    22: 'Red Bull',       23: 'Williams',27: 'Sauber',   30: 'RB',      31: 'Haas',
    43: 'Alpine',   44: 'Ferrari', 55: 'Williams', 63: 'Mercedes',81: 'McLaren',
    87: 'Haas'
}

# Team colors for Y-axis font
team_color_map = {
    'McLaren': '#FF8000',
    'Red Bull': '#00225E',
    'Ferrari': '#DC0000',
    'Mercedes': '#00D2BE',
    'Sauber': '#00E701',
    'Haas': '#B6BABD',
    'RB': '#FFFFFF',
    'Williams': '#266BEC',
    'Alpine': '#FF87BC',
    'Aston': '#00665E'
}

def generate_full_stint_plot(stint_data):
    if not stint_data:
        return {"data": [], "layout": go.Layout(title="No Stint Data")}

    # Collect latest driver/team mapping
    driver_set = sorted(set([s["driver_number"] for s in stint_data]))
    driver_sorted = sorted(driver_set, key=lambda d: driver_team_map.get(d, 'ZZZ') + f"{d:03}")
    driver_to_y = {driver: idx for idx, driver in enumerate(driver_sorted)}
    y_labels = [f"Driver {d}" for d in driver_sorted]

    traces = []
    for stint in stint_data:
        driver = stint["driver_number"]
        y_pos = driver_to_y[driver]
        lap_start = stint["lap_start"]
        lap_end = stint["lap_end"]
        compound = stint.get("compound", "UNKNOWN").upper()
        tyre_age = stint.get("tyre_age_at_start", 0)
        color = compound_colors.get(compound, "#888888")

        traces.append(go.Bar(
            x=[lap_end - lap_start + 1],
            y=[y_pos],
            base=lap_start,
            orientation='h',
            marker=dict(color=color, line=dict(color='black', width=1)),
            hovertemplate=(
                f"Driver {driver}<br>"
                f"Laps {lap_start}–{lap_end}<br>"
                f"Compound: {compound}<br>"
                f"Tyre Age: {tyre_age} laps"
                "<extra></extra>"
            ),
            showlegend=False
        ))

    # Font colors per driver for Y-axis labels
    yaxis_tickfont_colors = [team_color_map.get(driver_team_map.get(d, ''), 'white') for d in driver_sorted]

    layout = go.Layout(
        title="Tyre Stints by Driver (Grouped by Team)",
        paper_bgcolor='#111111',
        plot_bgcolor='#111111',
        font=dict(color='white'),
        barmode='overlay',
        xaxis=dict(
            title='Lap Number',
            tickfont=dict(color='white'),
            gridcolor='#444',
            zeroline=False
        ),
        yaxis=dict(
            tickvals=list(range(len(y_labels))),
            ticktext=[""] * len(y_labels),
            showticklabels=False,
            gridcolor='#444'
        ),
        margin=dict(t=60, l=100, r=40, b=60),
        height=max(400, 30 * len(y_labels)),
        annotations=[
            dict(
                xref='paper',
                yref='y',
                x=-0.008,
                y=i,
                text=label,
                font=dict(color=color, size=13),
                showarrow=False,
                xanchor='right'
            )
            for i, (label, color) in enumerate(zip(y_labels, yaxis_tickfont_colors))
            ]
    )


    return {"data": traces, "layout": layout}
