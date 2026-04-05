import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_bootstrap_templates import load_figure_template

load_figure_template("darkly")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    html.H1("Pitwall Telemetry")
], fluid=True, style={
    "minHeight": "100vh",
    "padding": "20px"
})

if __name__ == "__main__":
    app.run(debug=True)
