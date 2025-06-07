from dash import html
from datetime import datetime

def get_latest_message(message_data):
    if not message_data:
        return html.Div("No messages available", style=box_style("No Data"))

    # Convert ISO date strings to datetime objects and sort
    sorted_data = sorted(message_data, key=lambda x: datetime.fromisoformat(x["date"]))
    latest = sorted_data[-1]

    message_text = latest.get("message", "No message")
    time = latest.get("date", "")[-8:]  # Extract just the HH:MM:SS from timestamp

    return html.Div(
        [
            html.Strong("Latest Message:"),
            html.P(f"{message_text}", style={'margin': '5px 0'}),
            html.Small(f"Time: {time}", style={'fontStyle': 'italic', 'fontSize': '12px'})
        ],
        style=box_style(message_text)
    )

def box_style(message):
    return {
        'backgroundColor': '#444',
        'borderRadius': '12px',
        'padding': '15px',
        'marginBottom': '20px',
        'color': 'white',
        'boxShadow': '0 4px 10px rgba(0,0,0,0.4)',
        'maxWidth': '500px',
        'fontFamily': 'Arial',
    }
