# src/components/histogram_salary_range.py

import plotly.graph_objects as go
import pandas as pd
from dash import html, dcc


def create_histogram_by_salary_range(df: pd.DataFrame) -> html.Div:
    """
    Crée un histogramme des villes par intervalle de salaires médians

    Args:
        df (pd.DataFrame): Les données 

    Returns:
        html.Div: Un composant contenant le graphique 
    """
    if "DEC_MED18" not in df.columns:
        raise ValueError("La colonne 'DEC_MED18' est absente des données")

    # Création des intervalles de salaires (
    max_salary = int(df["DEC_MED18"].max())
    bins = list(range(0, max_salary + 2500, 2500))
    labels = [f"{x}-{x+2500}" for x in bins[:-1]]

    df["salary_range"] = pd.cut(df["DEC_MED18"], bins=bins, labels=labels)

    # Comptage du nombre de villes dans chaque intervalle
    salary_counts = df["salary_range"].value_counts().sort_index()

    fig = go.Figure(
        data=[
            go.Bar(
                x=salary_counts.index,
                y=salary_counts.values,
                marker=dict(color="#3498db"),
                  
            )
        ]
    )

    fig.update_layout(
        title={
            "text": "",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20, "family": "Arial, sans-serif", "color": "#2c3e50"},
        },
        xaxis=dict(
            title="Intervalle de Salaires (€)",
            tickangle=45,
            title_font={"size": 16, "family": "Arial, sans-serif"},
            tickfont={"size": 14, "family": "Arial, sans-serif"},
        ),
        yaxis=dict(
            title="Nombre de Villes",
            title_font={"size": 16, "family": "Arial, sans-serif"},
            tickfont={"size": 14, "family": "Arial, sans-serif"},
        ),
        plot_bgcolor="#f8f9fa",  
        paper_bgcolor="white",  
        margin=dict(l=40, r=40, t=60, b=40),
    )

    return html.Div(
        children=[
            html.H3(
                "Nombre de Villes par Intervalle de Salaires Médians en IDF tranche 2500€",
                style={
                    "text-align": "center",
                    "color": "#2c3e50",
                    "margin-bottom": "20px",
                },
            ),
            dcc.Graph(figure=fig),
            html.H4(
                "Le graphique montre que les villes avec un salaire médian compris entre 20 000€ "
                "et 35 000€",
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
