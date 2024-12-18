# src/components/histogram_salary_range.py
import plotly.graph_objects as go
import pandas as pd
from dash import html, dcc

def create_histogram_by_salary_range(df):
    # Créer des intervalles de salaires (de 0 à 5000, 5000 à 10000, etc.)
    bins = list(range(0, int(df["DEC_MED18"].max()) + 5000, 5000))
    df["salary_range"] = pd.cut(df["DEC_MED18"], bins=bins, labels=[f"{x}-{x+5000}" for x in bins[:-1]])
    
    # Compter le nombre de villes dans chaque intervalle
    salary_counts = df["salary_range"].value_counts().sort_index()

    # Créer un histogramme
    fig = go.Figure(data=[go.Bar(
        x=salary_counts.index,
        y=salary_counts.values,
        marker=dict(color='lightblue')
    )])

    fig.update_layout(
        title="Nombre de Villes par Intervalle de Salaires Médians",
        xaxis_title="Intervalle de Salaires (€)",
        yaxis_title="Nombre de Villes",
    )
    
    return html.Div([
        html.H3("Histogramme des Villes par Intervalle de Salaires Médians"),
        dcc.Graph(figure=fig)
    ])
