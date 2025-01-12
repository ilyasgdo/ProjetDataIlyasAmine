import plotly.express as px
import pandas as pd
from dash import dcc

def generate_heatmap_chomage(df: pd.DataFrame) -> dcc.Graph:
    """
    Génère une carte de chaleur montrant la part des indemnités de chômage par rapport au salaire médian.

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données.

    Returns:
        dcc.Graph: Le composant Dash contenant la carte de chaleur.
    """
    fig = px.density_heatmap(
        df,
        x="DEC_MED18",
        y="DEC_PCHO18",
        color_continuous_scale="Blues",
        title="Carte de chaleur : Part des indemnités de chômage vs Salaire médian",
        labels={
            "DEC_MED18": "Salaire Médian (€)",
            "DEC_PCHO18": "Part des indemnités de chômage (%)",
        },
    )
    return dcc.Graph(figure=fig)
