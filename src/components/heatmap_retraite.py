import plotly.express as px
import pandas as pd
from dash import dcc

def generate_heatmap_retraite(df: pd.DataFrame) -> dcc.Graph:
    """
    Génère une carte de chaleur montrant la part des pensions, retraites et rentes par rapport au salaire médian.

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données.

    Returns:
        dcc.Graph: Le composant Dash contenant la carte de chaleur.
    """
    fig = px.density_heatmap(
        df,
        x="DEC_MED18",
        y="DEC_PPEN18",
        color_continuous_scale="Viridis",
        title="Carte de chaleur : Part des pensions/retraites vs Salaire médian",
        labels={
            "DEC_MED18": "Salaire Médian (€)",
            "DEC_PPEN18": "Part des pensions/retraites (%)",
        },
    )
    return dcc.Graph(figure=fig)
