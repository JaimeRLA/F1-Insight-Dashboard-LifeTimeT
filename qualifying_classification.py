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
    rows = []
    for i, row in enumerate(df.itertuples(), start=1):
        time_str = f"{row.calculated_lap_time:.3f}s"
        color = {
            "Q1": "lightyellow",
            "Q2": "lightskyblue",
            "Q3": "lightgreen"
        }.get(row.session, "white")
        rows.append(html.Tr([
            html.Td(i),
            html.Td(row.driver_number),
            html.Td(row.session),
            html.Td(time_str)
        ], style={"backgroundColor": color}))

    return html.Table([
        html.Thead(html.Tr([
            html.Th("Pos"), html.Th("Driver"), html.Th("Session"), html.Th("Best Lap")
        ])),
        html.Tbody(rows)
    ])
