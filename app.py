import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from dashboard.components import InstallationSelect, Logo, Nav, Subtitle, Title
from dashboard.components.time_range_select import TimeRangeSelect
from dashboard.components.y_axis_select import YAxisSelect
from dashboard.graphs import plot_connections_statistics


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Aerosense Dashboard"
server = app.server


app.layout = html.Div(
    [
        dcc.Store(id="click-output"),
        html.Div(
            [
                html.Div(
                    [
                        Logo(app.get_asset_url("logo.png")),
                        Title(),
                        Subtitle(),
                    ]
                ),
                Nav(),
                html.Label("Installation reference"),
                InstallationSelect(),
                html.Label("Y-axis to plot"),
                YAxisSelect(),
                html.Label("Time range"),
                TimeRangeSelect(),
                html.Button("Get latest data", id="refresh-button", n_clicks=0),
            ],
            className="four columns sidebar",
        ),
        html.Div(
            [
                html.Div([dcc.Markdown(id="text")], className="text-box"),
                dcc.Graph(id="graph", style={"margin": "0px 20px", "height": "45vh"}),
            ],
            id="page",
            className="eight columns",
        ),
    ],
    className="row flex-display",
    style={"height": "100vh"},
)


@app.callback(
    Output("graph", "figure"),
    Input("installation_select", "value"),
    Input("y_axis_select", "value"),
    Input("time_range_select", "value"),
    Input("refresh-button", "n_clicks"),
)
def plot_connections_statistics_graph(installation_reference, y_axis_column, time_range, refresh):
    return plot_connections_statistics(installation_reference, y_axis_column, time_range)


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
