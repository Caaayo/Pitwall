import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.graph_objects as go
from data.parser import load_ibt, get_laps

def build_speed_trace(lap_a, lap_b):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=lap_a["LapDistPct"],
        y=lap_a["SpeedMph"],
        name=f"Lap {lap_a['Lap'].iloc[0]}",
    ))
    fig.add_trace(go.Scatter(
        x=lap_b["LapDistPct"],
        y=lap_b["SpeedMph"],
        name=f"Lap {lap_b['Lap'].iloc[0]}",
    ))
    fig.update_layout(
        template="plotly_dark",
        title="Speed Trace",
        title_x=0.5,
        xaxis_title="Track Position",
        yaxis_title="Speed (mph)",
    )
    return fig

def build_input_trace(lap_a, lap_b):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=lap_a["LapDistPct"],
        y=lap_a["Throttle"],
        name=f"Lap {lap_a['Lap'].iloc[0]} - Throttle",
        line=dict(color="#22c55e"),
    ))
    fig.add_trace(go.Scatter(
        x=lap_a["LapDistPct"],
        y=lap_a["Brake"],
        name=f"Lap {lap_a['Lap'].iloc[0]} - Brake",
        line=dict(color="#f43f5e"),
    ))
    fig.add_trace(go.Scatter(
        x=lap_b["LapDistPct"],
        y=lap_b["Throttle"],
        name=f"Lap {lap_b['Lap'].iloc[0]} - Throttle",
        line=dict(color="#22c55e", dash="dot"),
    ))
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
        yaxis_title="Brake / Throttle (%)",
    )
    return fig

def build_delta_trace(lap_a, lap_b):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=lap_a["LapDistPct"],
        y=lap_a["LapDeltaToBestLap"],
        name=f"Lap {lap_a['Lap'].iloc[0]}",
        fill="tozeroy",
        line=dict(color="#00FF00"),
        fillcolor="rgba(76, 132, 20, 0.15)",
    ))
    fig.add_trace(go.Scatter(
        x=lap_b["LapDistPct"],
        y=lap_b["LapDeltaToBestLap"],
        name=f"Lap {lap_b['Lap'].iloc[0]}",
        fill="tozeroy",
        line=dict(color="#FF0000"),
        fillcolor="rgba(128, 5, 23, 0.15)",
    ))
    fig.add_hline(y=0, line=dict(color="white", dash="dot", width=1))
    fig.update_layout(
        template="plotly_dark",
        title="Lap Delta to Best Lap",
        title_x=0.5,
        xaxis_title="Track Position",
        yaxis_title="Delta (sec)",
    )
    return fig

def build_track_map(lap_a):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=lap_a["Lon"],
        y=lap_a["Lat"],
        mode="markers",
        name=f"Lap {lap_a['Lap'].iloc[0]}",
        marker=dict(
            color=lap_a["SpeedMph"],
            colorscale="RdYlGn",
            size=3,
            colorbar=dict(title="mph"),
        ),
    ))
    fig.update_layout(
        template="plotly_dark",
        title="Track Map",
        title_x=0.5,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig

def build_corner_table(corner_df):
    fig = go.Figure(go.Table(
        header=dict(
            values=list(corner_df.columns),
            fill_color="#1e2130",
            font=dict(color="white", size=12),
            align="center",
        ),
        cells=dict(
            values=[corner_df[col] for col in corner_df.columns],
            fill_color="#0d1117",
            font=dict(color="white", size=11),
            align="center",
        ),
    ))
    fig.update_layout(
        template="plotly_dark",
        title="Corner Summary",
        title_x=0.5,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    return fig

if __name__ == "__main__":
    df = load_ibt("./ibtfiles/test_porschegt4_sonoma.ibt")
    laps = get_laps(df)
    fig = build_speed_trace(laps[2], laps[3])
    fig.show()