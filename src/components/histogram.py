# src/components/histogram.py
import plotly.express as px
import pandas as pd
from dash import html, dcc

def create_histogram(df):
    fig = px.histogram(df, x="DEC_MED18", title="Distribution des Salaires Médians",
                       labels={"DEC_MED18": "Salaire Médian (€)"}, nbins=10)
    fig.update_layout(bargap=0.1)
    
    return html.Div([
        html.H3("Histogramme des Salaires Médians"),
        dcc.Graph(figure=fig)
    ])
