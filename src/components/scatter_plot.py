# src/components/scatter_plot.py
import plotly.express as px
import pandas as pd
from dash import dcc

def generate_scatter_plot(filtered_df: pd.DataFrame, x_type: str, y_type: str) -> dcc.Graph:
    fig = px.scatter(
        filtered_df,
        x=x_type,
        y=y_type,
        color="LIBCOM",
        size="DEC_Q318",
        hover_name="LIBIRIS",
        title=f"Relation entre {x_type} et {y_type}",
        labels={x_type: x_type, y_type: y_type}
    )
    return dcc.Graph(id="scatter-plot", figure=fig)
