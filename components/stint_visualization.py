import plotly.graph_objs as go

compound_colors = {
    "SOFT": "#FF4C4C",
    "MEDIUM": "#FFD700",
    "HARD": "#FFFFFF",
}

def generate_stint_visualization(stint_data, driver_number=55):
    driver_stints = [s for s in stint_data if s.get("driver_number") == driver_number]
    if not driver_stints:
        return {'data': [], 'layout': go.Layout(title='No Stint Data')}

    traces = []
    for stint in driver_stints:
        x0 = stint["lap_start"]
        x1 = stint["lap_end"]
        compound = stint.get("compound", "UNKNOWN").upper()
        color = compound_colors.get(compound, "#999999")

        traces.append(
            go.Bar(
                x=[x1 - x0 + 1],
                y=[f"Lap {x0}-{x1}"],
                base=x0,
                orientation='h',
                marker=dict(color=color, line=dict(color='black', width=1)),
                hovertemplate=f"Laps {x0}–{x1}<br>Compound: {compound}<extra></extra>",
                showlegend=False,
            )
        )

    return {
        'data': traces,
        'layout': go.Layout(
            title=f"Tyre Stints – Driver {driver_number}",
            paper_bgcolor='#111111',
            plot_bgcolor='#111111',
            font=dict(color='white'),
            barmode='overlay',
            xaxis=dict(title='Lap Number', tickfont=dict(color='white'), gridcolor='#444'),
            yaxis=dict(showticklabels=False),
            margin=dict(t=60, l=60, r=40, b=60),
            height=200,
        )
    }
