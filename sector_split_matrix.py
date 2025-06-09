import pandas as pd
from dash import dash_table
import dash_html_components as html


def get_latest_laps_with_nulls(lap_data):
    df = pd.DataFrame(lap_data)
    df = df[~df['is_pit_out_lap']]
    df = df.sort_values(['driver_number', 'lap_number'], ascending=[True, False])
    df = df.drop_duplicates(subset='driver_number', keep='first')
    return df


def format_lap_time(seconds: float) -> str:
    if pd.isnull(seconds):
        return "No Time"
    minutes = int(seconds // 60)
    remainder = seconds % 60
    return f"{minutes}:{remainder:06.3f}"


def get_sector_color_from_minis(segments):
    if not isinstance(segments, list):
        return None
    counts = {'purple': 0, 'green': 0, 'yellow': 0}
    for val in segments:
        if val == 2051:
            counts['purple'] += 1
        elif val == 2049:
            counts['green'] += 1
        elif val == 2048:
            counts['yellow'] += 1
    if sum(counts.values()) == 0:
        return None
    return max(counts, key=counts.get)


def generate_sector_split_matrix(lap_data):
    try:
        # Team & color mappings
        driver_team_map = {
            4: 'McLaren', 81: 'McLaren',
            1: 'Red Bull', 22: 'Red Bull',
            16: 'Ferrari', 44: 'Ferrari',
            63: 'Mercedes', 12: 'Mercedes',
            5: 'Sauber', 27: 'Sauber',
            31: 'Haas', 87: 'Haas',
            30: 'RB', 6: 'RB',
            55: 'Williams', 23: 'Williams',
            10: 'Alpine', 43: 'Alpine',
            14: 'Aston', 18: 'Aston'
        }

        team_color_map = {
            'McLaren': '#FF8000',
            'Red Bull': "#00225E",
            'Ferrari': '#DC0000',
            'Mercedes': '#00D2BE',
            'Sauber': '#00E701',
            'Haas': '#B6BABD',
            'RB': '#FFFFFF',
            'Williams': "#266BEC",
            'Alpine': '#FF87BC',
            'Aston': '#00665E'
        }

        df = get_latest_laps_with_nulls(lap_data)
        df['Team'] = df['driver_number'].map(driver_team_map)
        df = df.sort_values(by='Team', kind='stable').reset_index(drop=True)

        df['S1'] = df['duration_sector_1']
        df['S2'] = df['duration_sector_2']
        df['S3'] = df['duration_sector_3']

        df['sector_color_s1'] = df['segments_sector_1'].apply(get_sector_color_from_minis)
        df['sector_color_s2'] = df['segments_sector_2'].apply(get_sector_color_from_minis)
        df['sector_color_s3'] = df['segments_sector_3'].apply(get_sector_color_from_minis)

        df['Outlap'] = df['is_pit_out_lap'].apply(lambda x: 'TRUE' if x else 'FALSE')

        def calc_total(row):
            if pd.notnull(row['S1']) and pd.notnull(row['S2']) and pd.notnull(row['S3']):
                return format_lap_time(row['S1'] + row['S2'] + row['S3'])
            return "No Time"

        df['Total Time'] = df.apply(calc_total, axis=1)

        # Table data
        table_data = df[['driver_number', 'S1', 'S2', 'S3', 'Total Time', 'Outlap']].copy()
        table_data.columns = ['Driver', 'S1', 'S2', 'S3', 'Total Time', 'Outlap']

        for col in ['S1', 'S2', 'S3']:
            table_data[col] = table_data[col].apply(lambda x: round(x, 3) if pd.notnull(x) else "No Time")

        # Color styling
        color_map = {
            'purple': '#8000FF',
            'green': '#00FF00',
            'yellow': '#FFFF00'
        }

        text_map = {
            'purple': 'white',
            'green': 'black',
            'yellow': 'black'
        }

        style_data_conditional = []

        for i, row in df.iterrows():
            driver = row['driver_number']
            for sector, color_col in zip(['S1', 'S2', 'S3'], ['sector_color_s1', 'sector_color_s2', 'sector_color_s3']):
                val = row[sector]
                color = row[color_col]
                if pd.isnull(val) or color is None:
                    continue
                style_data_conditional.append({
                    'if': {
                        'filter_query': f'{{Driver}} = {driver} && {{{sector}}} = {round(val, 3)}',
                        'column_id': sector
                    },
                    'backgroundColor': color_map.get(color, '#444'),
                    'color': text_map.get(color, 'white')
                })

        for i, row in df.iterrows():
            driver = row['driver_number']
            team = driver_team_map.get(driver)
            team_color = team_color_map.get(team)
            if team_color:
                font_color = 'white' if team in ['Williams', 'Red Bull', 'Aston', 'Ferrari'] else 'black'
                style_data_conditional.append({
                    'if': {
                        'filter_query': f'{{Driver}} = {driver}',
                        'column_id': 'Driver'
                    },
                    'backgroundColor': team_color,
                    'color': font_color
                })

        # Outlap column styling
        for i, row in df.iterrows():
            driver = row['driver_number']
            status = row['Outlap']
            style_data_conditional.append({
                'if': {
                    'filter_query': f'{{Driver}} = {driver}',
                    'column_id': 'Outlap'
                },
                'backgroundColor': '#00FF00' if status == 'TRUE' else '#FF4C4C',
                'color': 'black'
            })

        return html.Div(
            style={'padding': '20px', 'backgroundColor': '#111111', 'borderRadius': '10px'},
            children=[
                html.H2("Latest Lap Times by Driver", style={
                    'color': 'white',
                    'textAlign': 'center',
                    'marginBottom': '10px',
                    'fontFamily': 'Arial'
                }),
                html.P("Includes last valid lap with sector performance and team color indicators.",
                       style={'textAlign': 'center', 'color': '#ccc', 'marginBottom': '20px'}),
                dash_table.DataTable(
                    id='sector-table',
                    columns=[{"name": col, "id": col} for col in table_data.columns],
                    data=table_data.to_dict('records'),
                    style_cell={
                        'backgroundColor': '#111111',
                        'color': 'white',
                        'textAlign': 'center',
                        'padding': '8px',
                        'fontFamily': 'Arial',
                        'fontSize': '14px',
                    },
                    style_header={
                        'backgroundColor': '#111111',
                        'fontWeight': 'bold',
                        'color': 'white',
                        'borderBottom': '1px solid #444',
                        'fontSize': '15px'
                    },
                    style_data_conditional=style_data_conditional,
                    style_table={
                        'overflowX': 'auto',
                        'border': '1px solid #333',
                        'borderRadius': '8px',
                        'boxShadow': '0 0 12px rgba(0,0,0,0.5)'
                    },
                )
            ]
        )
    except Exception as e:
        print(f"❌ ERROR en generate_sector_split_matrix: {e}")
        return html.Div(f"❌ Error generando la tabla: {e}", style={'color': 'red'})
