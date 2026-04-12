import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from dash_bootstrap_templates import load_figure_template
from data.parser import load_ibt, get_laps, get_lap_time
from components.charts import build_speed_trace, build_input_trace, build_delta_trace, build_track_map, build_corner_table

df = load_ibt("./ibtfiles/test_porschegt4_sonoma.ibt")
laps = get_laps(df)
lap_options = [{"label": f"Lap {k}", "value": k} for k in laps.keys()]

load_figure_template("darkly")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

def format_laptime(seconds):
    if seconds <= 0:
        return "--:--.---"
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}:{secs:06.3f}"

app.layout = dbc.Container([

    html.H1("Pitwall Telemetry", style={"textAlign": "center", "padding": "20px 0"}),

    dbc.Row([
        dbc.Col([
            html.Label("Lap A"),
            dcc.Dropdown(id="lap-a", options=lap_options, value=2, clearable=False, style={"color": "#000000"}),
        ]),
        dbc.Col([
            html.Label("Lap B"),
            dcc.Dropdown(id="lap-b", options=lap_options, value=3, clearable=False, style={"color": "#000000"}),
        ]),
    ], style={"marginBottom": "20px"}),

    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Best Lap", className="card-title"),
            html.H4(id="stat-best-lap"),
        ])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Lap A Time", className="card-title"),
            html.H4(id="stat-lap-a"),
        ])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Lap B Time", className="card-title"),
            html.H4(id="stat-lap-b"),
        ])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H6("Delta", className="card-title"),
            html.H4(id="stat-delta"),
        ])), width=3),
    ], style={"marginBottom": "20px"}),

    dbc.Row([
        dbc.Col(dcc.Graph(id="speed-chart"), width=12),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="input-chart"), width=12),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="delta-chart"), width=8),
        dbc.Col(dcc.Graph(id="track-map"), width=4),
    ]),
    # Corner Summary
    # dbc.Row([
    #     dbc.Col(dcc.Graph(id="corner-table"), width=12),
    # ]),

], fluid=True, style={"minHeight": "100vh", "padding": "20px"})

@app.callback(
    Output("speed-chart", "figure"),
    Output("input-chart", "figure"),
    Output("delta-chart", "figure"),
    Output("track-map", "figure"),
    # Output("corner-table", "figure"),
    Output("stat-best-lap", "children"),
    Output("stat-lap-a", "children"),
    Output("stat-lap-b", "children"),
    Output("stat-delta", "children"),
    Input("lap-a", "value"),
    Input("lap-b", "value"),
)
def update_charts(lap_a_value, lap_b_value):
    if lap_a_value is None or lap_b_value is None:
        return [dash.no_update] * 9

    lap_a = laps[lap_a_value]
    lap_b = laps[lap_b_value]

    speed_fig = build_speed_trace(lap_a, lap_b)
    input_fig = build_input_trace(lap_a, lap_b)
    delta_fig = build_delta_trace(lap_a, lap_b)
    map_fig = build_track_map(lap_a)

    # corners = get_corners(lap_a)
    # corner_df = get_corner_summary(lap_a, lap_b, corners)
    # corner_fig = build_corner_table(corner_df)

    best_lap_time = min(get_lap_time(df, lap_num) for lap_num in laps.keys())
    best_lap = format_laptime(best_lap_time)
    lap_a_time = format_laptime(get_lap_time(df, lap_a_value))
    lap_b_time = format_laptime(get_lap_time(df, lap_b_value))
    delta = format_laptime(abs(get_lap_time(df, lap_b_value) - get_lap_time(df, lap_a_value)))

    return speed_fig, input_fig, delta_fig, map_fig, best_lap, lap_a_time, lap_b_time, delta

if __name__ == "__main__":
    app.run(debug=True)