from dash import dcc, html
import plotly.graph_objs as go
from datetime import datetime

def render_driver_position_line(position_data, driver_number):
    # Filter data for the driver
    driver_data = [
        p for p in position_data
        if p.get("driver_number") == driver_number and p.get("date") and p.get("position") is not None
    ]

    if not driver_data:
        return html.Div(f"No position data for driver {driver_number}", style={"color": "white"})

    # Parse dates
    for p in driver_data:
        p["parsed_date"] = datetime.fromisoformat(p["date"])

    # Get only latest day
    latest_date = max(p["parsed_date"].date() for p in driver_data)
    driver_data = [p for p in driver_data if p["parsed_date"].date() == latest_date]
    driver_data.sort(key=lambda x: x["parsed_date"])

    # Evenly spaced x values
    lap_indices = list(range(1, len(driver_data) + 1))
    positions = [p["position"] for p in driver_data]

    trace = go.Scatter(
        x=lap_indices,
        y=positions,
        mode='lines+markers',
        name='Track Position',
        line=dict(color='#00BFFF', width=3),
        marker=dict(color='white', size=8),
        hovertemplate="Lap %{x}<br>Position: %{y}<extra></extra>"
    )

    layout = go.Layout(
        title=f"Driver {driver_number} – Position per Lap (Estimated)",
        paper_bgcolor='#111111',
        plot_bgcolor='#111111',
        font=dict(color='white'),
        xaxis=dict(visible=False),  # ❌ Hides X-axis
        yaxis=dict(
            title='Track Position',
            autorange='reversed',
            tickfont=dict(color='white'),
            gridcolor='#444'
        ),
        margin=dict(t=50, l=60, r=40, b=60),
        hovermode='closest',
        height=500,
        showlegend=False
    )

    return html.Div([
        dcc.Graph(
            figure=go.Figure(data=[trace], layout=layout),
            config={'displayModeBar': False}
        )
    ])
