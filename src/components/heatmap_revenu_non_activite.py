import plotly.express as px
import pandas as pd
from dash import dcc

def generate_heatmap_revenu_non_salarie(df: pd.DataFrame) -> dcc.Graph:
    """
    Génère une carte de chaleur montrant les parts de revenus des activités non salariées 
    et des autres revenus par rapport au salaire médian.

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données.

    Returns:
        dcc.Graph: Le composant Dash contenant la carte de chaleur.
    """
    fig = px.density_heatmap(
        df,
        x="DEC_MED18",
        y="DEC_PAUT18",
        z="DEC_PCHO18",
        color_continuous_scale="Cividis",
        title="Carte de chaleur : Revenus non liés à l'activité et autres par rapport au salaire médian",
        labels={
            "DEC_MED18": "Salaire Médian (€)",
            "DEC_PAUT18": "Part des autres revenus (%)",
            "DEC_PCHO18": "Part des revenus non-salariés (%)",
        },
    )
    return dcc.Graph(figure=fig)
