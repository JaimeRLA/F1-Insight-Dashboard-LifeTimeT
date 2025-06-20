from dash import html, dcc

def get_layout():

    card_style = {
        'backgroundColor': "#111111",
        'borderRadius': '16px',
        'padding': '20px',
        'marginBottom': '20px',
        'boxShadow': '0 4px 10px rgba(0,0,0,0.5)'
    }

    return html.Div(
        style={'backgroundColor': '#111111', 'padding': '40px', 'fontFamily': 'Arial'},
        children=[
            # 🏁 Combined Header: Event Info + Circuit Map
            html.Div(id='dashboard-header', style={'marginBottom': '40px'}),

            # Graphs Section
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='stint-visualization', figure={}, config={'displayModeBar': False})
                    ], style=card_style),

                    html.Div([
                        html.Div(id='qualifying-classification-box')
                    ], style=card_style)

                ], style={'flex': '1', 'marginRight': '20px'}),

                html.Div([
                    html.Div([
                        dcc.Graph(id='mini-sector-matrix', figure={}, config={'displayModeBar': False})
                    ], style=card_style),

                    html.Div([
                        html.Div(id='sector-split-matrix')
                    ], style=card_style)

                ], style={'flex': '1'})
            ], style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'wrap'}),

            # Stores
            dcc.Store(id='lap-data-store'),
            dcc.Store(id='stint-data-store'),
            dcc.Store(id='weather-data-store'),
            dcc.Store(id='position-data-store'),
            dcc.Store(id='meeting-data-store'),
            dcc.Store(id='message-data-store'),

            # Interval
            dcc.Interval(
                id='live-update-interval',
                interval=100 * 1000,
                n_intervals=0
            )
        ]
    )
