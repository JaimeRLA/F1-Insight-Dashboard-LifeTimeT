from dash import html
import pandas as pd
from datetime import datetime


def classify_sessions(laps, messages):
    flags = sorted([msg for msg in messages if msg.get("flag") == "CHEQUERED"],
                   key=lambda x: x["date"])

    df = pd.DataFrame(laps)

    # Recalcular tiempo total desde sectores
    df = df.dropna(subset=['duration_sector_1', 'duration_sector_2', 'duration_sector_3']).copy()
    df["calculated_lap_time"] = (
        df["duration_sector_1"] + df["duration_sector_2"] + df["duration_sector_3"]
    )

    df['date_start'] = pd.to_datetime(df['date_start'])
    cuts = [datetime.fromisoformat(f["date"].replace("Z", "+00:00")) for f in flags]

    def assign_session(row):
        if len(cuts) == 0 or row['date_start'] < cuts[0]:
            return "Q1"
        elif len(cuts) == 1 or row['date_start'] < cuts[1]:
            return "Q2"
        else:
            return "Q3"

    df["qualifying_session"] = df.apply(assign_session, axis=1)
    return df, len(cuts)


def build_live_qualifying_result(df, current_phase):
    df = df.copy()

    # === Q1 ===
    q1 = df[df["qualifying_session"] == "Q1"]
    best_q1 = q1.groupby("driver_number")["calculated_lap_time"].min().reset_index()
    best_q1["session"] = "Q1"
    best_q1 = best_q1.sort_values("calculated_lap_time").reset_index(drop=True)

    if current_phase == 0:
        return best_q1.assign(eliminated=False)

    # === Q2 ===
    q2_drivers = best_q1.head(15)["driver_number"]
    q2 = df[(df["qualifying_session"] == "Q2") & (df["driver_number"].isin(q2_drivers))]
    best_q2 = q2.groupby("driver_number")["calculated_lap_time"].min().reset_index()
    best_q2["session"] = "Q2"
    best_q2 = best_q2.sort_values("calculated_lap_time").reset_index(drop=True)

    if current_phase == 1:
        return best_q2.assign(eliminated=False)

    # === Q3 ===
    q3_drivers = best_q2.head(10)["driver_number"]
    q3 = df[(df["qualifying_session"] == "Q3") & (df["driver_number"].isin(q3_drivers))]
    best_q3 = q3.groupby("driver_number")["calculated_lap_time"].min().reset_index()
    best_q3["session"] = "Q3"
    best_q3 = best_q3.sort_values("calculated_lap_time").reset_index(drop=True)

    return best_q3.assign(eliminated=False)

def render_qualifying_table(df):
    # Team color setup
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

    rows = []
    for i, row in enumerate(df.itertuples(), start=1):
        minutes = int(row.calculated_lap_time // 60)
        seconds = row.calculated_lap_time % 60
        time_str = f"{minutes}:{seconds:06.3f}"

        background_color = {
            "Q1": "#000000",
            "Q2": "#000000",
            "Q3": "#000000"
        }.get(row.session, "#000000")

        team = driver_team_map.get(row.driver_number)
        team_color = team_color_map.get(team, "white")

        rows.append(html.Tr([
            html.Td(i, style={"padding": "12px", "fontWeight": "bold", "color": "white", "border": "1px solid white"}),
            html.Td(
                row.driver_number,
                style={"padding": "12px", "color": team_color, "fontWeight": "bold", "border": "1px solid white"}
            ),
            html.Td(row.session, style={"padding": "12px", "color": "white", "border": "1px solid white"}),
            html.Td(time_str, style={"padding": "12px", "color": "white", "border": "1px solid white"})
        ], style={
            "backgroundColor": background_color,
            "fontSize": "16px",
            "textAlign": "center"
        }))

    return html.Div([
        html.H2("Live Qualifying Leaderboard", style={
            "color": "white",
            "textAlign": "center",
            "marginBottom": "20px",
            "fontFamily": "Arial"
        }),
        html.Table([
            html.Thead(html.Tr([
                html.Th("Pos", style={"padding": "12px", "color": "white", "fontSize": "18px", "border": "1px solid white"}),
                html.Th("Driver", style={"padding": "12px", "color": "white", "fontSize": "18px", "border": "1px solid white"}),
                html.Th("Session", style={"padding": "12px", "color": "white", "fontSize": "18px", "border": "1px solid white"}),
                html.Th("Best Lap", style={"padding": "12px", "color": "white", "fontSize": "18px", "border": "1px solid white"})
            ], style={"backgroundColor": "#000000"})),
            html.Tbody(rows)
        ], style={
            "width": "100%",
            "borderCollapse": "collapse",
            "backgroundColor": "#000000",
            "border": "1px solid white",
            "borderRadius": "8px",
            "boxShadow": "0 0 10px rgba(255,255,255,0.1)",
            "fontFamily": "Arial"
        })
    ], style={"padding": "20px"})
