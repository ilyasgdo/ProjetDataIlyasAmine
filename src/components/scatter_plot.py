# src/components/scatter_plot.py
import plotly.express as px
import pandas as pd
from dash import dcc

def generate_scatter_plot(df: pd.DataFrame) -> dcc.Graph:
    fig = px.scatter(
        df,
        x="DEC_MED18",
        y="DEC_GI18",
        color="LIBCOM",
        size="DEC_Q318",
        hover_name="LIBIRIS",
        title="Relation entre le salaire médian et l'indice de Gini",
        labels={"DEC_MED18": "Salaire Médian (€)", "DEC_GI18": "Indice de Gini", "DEC_Q318": "Quantile Q3"}
    )
    return dcc.Graph(figure=fig)
