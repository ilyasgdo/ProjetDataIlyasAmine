import pandas as pd
import plotly.express as px
from dash import dcc, Dash, Input, Output
import dash_bootstrap_components as dbc

def create_dynamic_scatter_plot(app: Dash, df: pd.DataFrame) -> dbc.Col:
    """
    Crée un graphique de dispersion interactif avec des sélecteurs pour les axes X et Y.

    Args:
        app (Dash): L'application Dash.
        df (pd.DataFrame): Le DataFrame contenant les données.

    Returns:
        dbc.Col: Le composant Dash contenant le graphique de dispersion.
    """
    @app.callback(
        Output("dynamic-scatter-plot", "figure"),
        [Input("scatter-x-axis", "value"), Input("scatter-y-axis", "value")]
    )
    def update_scatter_plot(x_axis: str, y_axis: str):
        fig = px.scatter(
            df,
            x=x_axis,
            y=y_axis,
            color="LIBCOM",
            title=f"Scatter Plot: {x_axis} vs {y_axis}",
            labels={x_axis: x_axis, y_axis: y_axis},
        )
        return fig

    return dbc.Col(
        children=[
            dcc.Dropdown(
                id="scatter-x-axis",
                options=[{"label": col, "value": col} for col in df.columns if df[col].dtype in [int, float]],
                value="DEC_MED18",
                clearable=False,
                style={"marginBottom": "10px"},
            ),
            dcc.Dropdown(
                id="scatter-y-axis",
                options=[{"label": col, "value": col} for col in df.columns if df[col].dtype in [int, float]],
                value="DEC_PAUT18",
                clearable=False,
                style={"marginBottom": "10px"},
            ),
            dcc.Graph(id="dynamic-scatter-plot"),
        ],
        width=6,
        className="mb-4",
    )
