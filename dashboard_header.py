from dash import html

def render_dashboard_header(meeting_data):
    if not meeting_data:
        return html.Div("No meeting data available", style={'color': 'white', 'textAlign': 'center'})

    info = meeting_data[0]
    meeting_name = info.get('meeting_official_name', '')
    location = info.get('location', '')
    country = info.get('country_name', '')
    track = info.get('circuit_short_name', '')
    date = info.get('date_start', '')[:10]
    gmt = info.get('gmt_offset', '')

    # Circuit image logic
    meeting_name_lower = meeting_name.lower()
    image_mapping = {
        'españa': 'spain.png',
        'canadian': 'canada.png',
        'canada': 'canada.png',
        # Add more as needed
    }

    selected_image = None
    for keyword, filename in image_mapping.items():
        if keyword in meeting_name_lower:
            selected_image = filename
            break

    image_component = html.Img(
        src=f"/assets/circuits/{selected_image}",
        style={
            "width": "100%",
            "maxWidth": "420px",
            "borderRadius": "12px",
            "boxShadow": "0 4px 12px rgba(0,0,0,0.6)"
        }
    ) if selected_image else html.Div("No circuit image available", style={"color": "#888"})

    # Layout with flexbox
    return html.Div([
        html.Div([
            html.H1(meeting_name, style={
                'color': 'white',
                'fontSize': '48px',
                'marginBottom': '10px'
            }),
            html.P(f"📍 {location}, {country}", style={'color': '#ccc', 'fontSize': '28px'}),
            html.P(f"🏁 Track: {track}", style={'color': '#ccc', 'fontSize': '28px'}),
            html.P(f"🗓️ Date: {date}", style={'color': '#ccc', 'fontSize': '28px'}),
            html.P(f"🕒 Local Offset: UTC+{gmt}", style={'color': '#ccc', 'fontSize': '28px'}),
        ], style={'flex': '1', 'paddingRight': '30px'}),

        html.Div(image_component, style={'flex': '0 0 auto'})
    ], style={
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'center',
        'justifyContent': 'space-between',
        'marginBottom': '40px',
        'padding': '0 20px'
    })
