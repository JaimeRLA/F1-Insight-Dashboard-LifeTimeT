from dash import html
from datetime import datetime

def render_driver_position_box(position_data, driver_number):
    # Filter data for the driver
    driver_data = [
        p for p in position_data
        if p.get("driver_number") == driver_number and p.get("date") and p.get("position") is not None
    ]

    if not driver_data:
        return html.Div(f"No position data for driver {driver_number}", style={"color": "white"})

    # Parse dates and get the latest position
    for p in driver_data:
        p["parsed_date"] = datetime.fromisoformat(p["date"])

    latest_entry = max(driver_data, key=lambda x: x["parsed_date"])
    latest_position = latest_entry["position"]
    latest_time = latest_entry["parsed_date"].strftime("%Y-%m-%d %H:%M:%S")

    # Display a styled box
    return html.Div([
        html.Div(f"Latest Position: {latest_position}", style={
            "fontSize": "36px",
            "fontWeight": "bold",
            "color": "#FFFFFF",
            "backgroundColor": "#222",
            "padding": "20px",
            "borderRadius": "10px",
            "boxShadow": "0px 0px 10px rgba(0, 191, 255, 0.7)",
            "textAlign": "center"
        }),
        html.Div(f"As of {latest_time}", style={"fontSize": "14px", "marginTop": "10px", "color": "#aaa"})
    ], style={"color": "white", "textAlign": "center"})
