import plotly.express as px
import pandas as pd
from dash import dcc,html

def generate_heatmap_revenu_non_salarie(df: pd.DataFrame) -> html.Div:
    """
    Génère une carte de chaleur montrant les parts de revenus des activités non salariées 
    et des autres revenus par rapport au salaire médian

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données

    Returns:
        html.Div: Le composant Dash contenant la carte de chaleur
    """
    fig = px.density_heatmap(
        df,
        x="DEC_MED18",
        y="DEC_PAUT18",
        z="DEC_PCHO18",
        color_continuous_scale="Cividis",
        title="",
        labels={
            "DEC_MED18": "Salaire Médian (€)",
            "DEC_PAUT18": "Part des autres revenus (%)",
            "DEC_PCHO18": "Part des revenus non-salariés (%)",
        },
    )
    
    return html.Div(
        children=[
            html.H3(
                "Carte de chaleur : Revenus non liés à l'activité et autres par rapport au salaire médian",
                style={
                    "text-align": "center",
                    "color": "#2c3e50",
                    "margin-bottom": "20px",
                },
            ),
            dcc.Graph(figure=fig),
            html.H4(
                "Nous pouvons constater que, plus le salaire médian augmente, plus les revenus "
                "non liés à l'activité augmentent, ce qui peut être expliqué par le fait qu'il y a "
                "plus de rentiers parmi ces personnes.",
                style={
                    "textAlign": "center",
                    "color": "#2c3e50",
                    "marginBottom": "20px",
                },
            )
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
