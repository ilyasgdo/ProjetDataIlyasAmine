# src/components/heatmap.py
import plotly.express as px
import pandas as pd
from dash import dcc


def generate_heatmap(df: pd.DataFrame) -> dcc.Graph:
    fig = px.density_heatmap(
        df,
        x="DEC_MED18",
        y="DEC_GI18",
        z="DEC_Q318",
        color_continuous_scale="Inferno",
        title="Carte de chaleur : Salaire médian, indice de Gini et quantile Q3",
        labels={
            "DEC_MED18": "Salaire Médian (€)",
            "DEC_GI18": "Indice de Gini",
            "DEC_Q318": "Quantile Q3",
        },
    )
    return dcc.Graph(figure=fig)
