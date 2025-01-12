# src/components/histogram.py
import plotly.express as px
from dash import html, dcc


def create_histogram(df):
    fig = px.histogram(
        df,
        x="DEC_MED18",
        title="Nombre de Villes par Intervalle de Salaires Médians en IDF tranche 10000",
        labels={"DEC_MED18": "Salaire Médian (€)"},
        nbins=30,
    )
    fig.update_layout(bargap=0.1)

    return html.Div(
        [html.H3("Histogramme des Salaires Médians"), dcc.Graph(figure=fig)]
    )
