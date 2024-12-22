# src/components/bar_chart.py
import plotly.express as px
import pandas as pd
from dash import dcc

def generate_bar_chart(df: pd.DataFrame) -> dcc.Graph:
    fig = px.bar(
        df,
        x="LIBIRIS",
        y="DEC_MED18",
        color="DEC_GI18",
        title="Salaire médian et indice de Gini par zone IRIS",
        labels={"LIBIRIS": "Zone IRIS", "DEC_MED18": "Salaire Médian (€)", "DEC_GI18": "Indice de Gini"},
        color_continuous_scale="Viridis"
    )
    return dcc.Graph(figure=fig)
