import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.graph_objects as go
from data.parser import load_ibt, get_laps

def build_speed_trace(lap_a, lap_b):
    fig = go.Figure()

    # Lap A Scatter trace
    fig.add_trace(go.Scatter(
        x=lap_a["LapDistPct"],
        y=lap_a["SpeedMph"],
        name=f"Lap: {lap_a['Lap'].iloc[0]}"
    ))

    # Lap B Scatter trace
    fig.add_trace(go.Scatter(
        x=lap_b["LapDistPct"],
        y=lap_b["SpeedMph"],
        name=f"Lap: {lap_b['Lap'].iloc[0]}"
    ))

    # Stylizing
    fig.update_layout(
        template="plotly_dark",
        title="Speed Trace",
        title_x=0.5,
        xaxis_title="Track Position",
        yaxis_title="Speed (mph)"
    )

    return fig

def build_input_trace(lap_a, lap_b):
    fig = go.Figure()

    # Lab A Throttle Scatter Trace
    fig.add_trace(go.Scatter(
        x=lap_a["LapDistPct"],
        y=lap_a["Throttle"],
        name=f"Lap {lap_a['Lap'].iloc[0]} - Throttle",
        line=dict(color="#22c55e"),
    ))
    # Lab A Brake Scatter Trace
    fig.add_trace(go.Scatter(
        x=lap_a["LapDistPct"],
        y=lap_a["Brake"],
        name=f"Lap {lap_a['Lap'].iloc[0]} - Brake",
        line=dict(color="#f43f5e"),
    ))

    # Lab B Throttle Scatter Trace
    fig.add_trace(go.Scatter(
        x=lap_b["LapDistPct"],
        y=lap_b["Throttle"],
        name=f"Lap {lap_b['Lap'].iloc[0]} - Throttle",
        line=dict(color="#22c55e", dash="dot"),
    ))
    # Lab B Brake Scatter Trace
    fig.add_trace(go.Scatter(
        x=lap_b["LapDistPct"],
        y=lap_b["Brake"],
        name=f"Lap {lap_b['Lap'].iloc[0]} - Brake",
        line=dict(color="#f43f5e", dash="dot"),
    ))

    fig.update_layout(
        template="plotly_dark",
        title="Brake / Throttle",
        title_x=0.5,
        xaxis_title="Track Position",
        yaxis_title="Brake / Throttle (%)"
    )

    return fig

def build_delta_trace(lap_a, lap_b):
    fig = go.Figure()

    # Lab A Lap Delta Scatter Trace
    fig.add_trace(go.Scatter(
        x=lap_a["LapDistPct"],
        y=lap_a["LapDeltaToBestLap"],
        name=f"Lap: {lap_a['Lap'].iloc[0]}",
        fill="tozeroy",
        line=dict(color="#00FF00"),
        fillcolor="rgba(76, 132, 20, 0.15)",
    ))
    # Lab B Lap Delta Scatter Trace
    fig.add_trace(go.Scatter(
        x=lap_b["LapDistPct"],
        y=lap_b["LapDeltaToBestLap"],
        name=f"Lap: {lap_b['Lap'].iloc[0]}",
        fill="tozeroy",
        line=dict(color="#FF0000"),
        fillcolor="rgba(128, 5, 23, 0.15)",
    ))

    fig.add_hline(y=0, line=dict(color="white", dash="dot", width=2))

    fig.update_layout(
        template="plotly_dark",
        title="Lap Delta to Best Lap",
        title_x=0.5,
        xaxis_title="Track Position",
        yaxis_title="Delta (sec)"
    )

    return fig

if __name__ == "__main__":

    df = load_ibt("./ibtfiles/test_porschegt4_sonoma.ibt")
    laps = get_laps(df)

    speed_fig = build_speed_trace(laps[1], laps[2])
    input_fig = build_input_trace(laps[1], laps[2])
    delta_fig = build_delta_trace(laps[1], laps[2])
    delta_fig.show()


