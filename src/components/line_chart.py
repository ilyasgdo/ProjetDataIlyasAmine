# src/components/line_chart.py
import plotly.express as px
import pandas as pd
from dash import dcc

def generate_line_chart(df: pd.DataFrame) -> dcc.Graph:
    fig = px.line(
        df,
        x="LIBIRIS",
        y=["DEC_D118", "DEC_D218", "DEC_D318", "DEC_D418"],
        title="Distribution des déciles par zone IRIS",
        labels={"value": "Déciles", "LIBIRIS": "Zone IRIS", "variable": "Type de Décile"}
    )
    return dcc.Graph(figure=fig)
