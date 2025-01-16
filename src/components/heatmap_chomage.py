import plotly.express as px
import pandas as pd
from dash import dcc,html

def generate_heatmap_chomage(df: pd.DataFrame) -> html.Div:
    """
    Génère une carte de chaleur montrant la part des indemnités de chômage par rapport au salaire médian

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données

    Returns:
        html.Div: Le composant Dash contenant la carte de chaleur
    """
    fig = px.density_heatmap(
        df,
        x="DEC_MED18",
        y="DEC_PCHO18",
        color_continuous_scale="Blues",
        labels={
            "DEC_MED18": "Salaire Médian (€)",
            "DEC_PCHO18": "Part des indemnités de chômage (%)",
        },
    )
    return html.Div(
        children=[
            html.H3(
                "Carte de chaleur : Part des indemnités de chômage vs Salaire médian",

                style={
                    "text-align": "center",
                    "color": "#2c3e50",
                    "margin-bottom": "20px",
                },
            ),
            dcc.Graph(figure=fig),
            html.H4(
                "Plus le salaire médian augmente, plus la part des indemnités de chômage diminue",
                style={
                    "textAlign": "center",
                    "color": "#2c3e50",
                    "marginBottom": "20px",
                },
            ),
        ],
        style={
            "padding": "20px",
            "background-color": "#ecf0f1",
            "border-radius": "10px",
            "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
            "max-width": "800px",
            "margin": "0 auto",
        },
    )
