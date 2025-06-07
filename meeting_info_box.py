from dash import html

def display_meeting_info(meeting_data):
    if not meeting_data:
        return html.Div("No meeting data available", style={'color': 'white'})

    info = meeting_data[0]  # Assuming one meeting only
    return html.Div([
        html.P(f"{info.get('meeting_official_name')}", style={'color': 'white', 'fontWeight': 'bold', 'fontSize': '18px'}),
        html.P(f"Location: {info.get('location')} - {info.get('country_name')}", style={'color': 'white'}),
        html.P(f"Track: {info.get('circuit_short_name')}", style={'color': 'white'}),
        html.P(f"Start Time (UTC): {info.get('date_start')}", style={'color': 'white'}),
        html.P(f"Local GMT Offset: UTC+{info.get('gmt_offset')}", style={'color': 'white'}),
        html.P(f"Year: {info.get('year')}", style={'color': 'white'})
    ], style={
        'backgroundColor': '#444',
        'borderRadius': '16px',
        'padding': '20px',
        'boxShadow': '0 4px 10px rgba(0,0,0,0.5)',
        'width': '410px',
        'marginBottom': '20px'
    })
