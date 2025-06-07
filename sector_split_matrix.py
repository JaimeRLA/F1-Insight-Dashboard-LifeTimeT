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
        df = get_latest_laps_with_nulls(lap_data)

        df['S1'] = df['duration_sector_1']
        df['S2'] = df['duration_sector_2']
        df['S3'] = df['duration_sector_3']
        df['Lap'] = df['lap_number']

        df['sector_color_s1'] = df['segments_sector_1'].apply(get_sector_color_from_minis)
        df['sector_color_s2'] = df['segments_sector_2'].apply(get_sector_color_from_minis)
        df['sector_color_s3'] = df['segments_sector_3'].apply(get_sector_color_from_minis)

        def calc_total(row):
            if pd.notnull(row['S1']) and pd.notnull(row['S2']) and pd.notnull(row['S3']):
                return format_lap_time(row['S1'] + row['S2'] + row['S3'])
            return "No Time"

        df['Total Time'] = df.apply(calc_total, axis=1)

        table_data = df[['driver_number', 'Lap', 'S1', 'S2', 'S3', 'Total Time']].copy()
        table_data.columns = ['Driver', 'Lap', 'S1', 'S2', 'S3', 'Total Time']

        # Redondear para mostrar
        for col in ['S1', 'S2', 'S3']:
            table_data[col] = table_data[col].apply(lambda x: round(x, 3) if pd.notnull(x) else "No Time")

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

        return html.Div([
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
                    'color': 'deepskyblue',
                    'borderBottom': '1px solid #444',
                },
                style_data_conditional=style_data_conditional,
                style_table={
                    'overflowX': 'auto',
                    'border': '1px solid #333',
                    'borderRadius': '8px',
                },
            )
        ])
    except Exception as e:
        print(f"❌ ERROR en generate_sector_split_matrix: {e}")
        return html.Div(f"❌ Error generando la tabla: {e}", style={'color': 'red'})
