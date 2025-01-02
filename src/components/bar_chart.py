# src/components/bar_chart.py
import plotly.express as px
import pandas as pd
from dash import dcc


def generate_bar_chart(filtered_df: pd.DataFrame, data_type: str) -> dcc.Graph:
    fig = px.bar(
        filtered_df,
        x="LIBIRIS",
        y=data_type,
        title=f"Graphique des données - {data_type}",
        labels={"LIBIRIS": "Zone IRIS", data_type: data_type},
        color=data_type,
        color_continuous_scale="Viridis",
    )
    return dcc.Graph(id="bar-chart", figure=fig)
