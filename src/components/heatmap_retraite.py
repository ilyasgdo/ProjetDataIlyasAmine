import plotly.express as px
import pandas as pd
from dash import dcc,html

def generate_heatmap_retraite(df: pd.DataFrame) -> html.Div:
    """
    Génère une carte de chaleur montrant la part des pensions, retraites et rentes par rapport au salaire médian.

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données.

    Returns:
        html.Div: Le composant Dash contenant la carte de chaleur.
    """
    fig = px.density_heatmap(
        df,
        x="DEC_MED18",
        y="DEC_PPEN18",
        color_continuous_scale="Viridis",
        labels={
            "DEC_MED18": "Salaire Médian (€)",
            "DEC_PPEN18": "Part des pensions/retraites (%)",
        },
    )
    return html.Div(
        children=[
            html.H3(
                "Carte de chaleur : Part des pensions/retraites vs Salaire médian",
                style={
                    "text-align": "center",
                    "color": "#2c3e50",
                    "margin-bottom": "20px",
                },
            ),
            dcc.Graph(figure=fig),
             html.H4(
                "La part des pensions/retraites est concentrée dans les communes avec un salaire médian autour de 20 000€ à 30 000€",
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