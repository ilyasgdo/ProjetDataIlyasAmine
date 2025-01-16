# src/components/histogram.py
import plotly.express as px
import pandas as pd
from dash import html, dcc


def create_histogram(df: pd.DataFrame)->html.Div:
    fig = px.histogram(
        df,
        x="DEC_MED18",
        title="Nombre de Villes par Intervalle de Salaires Médians en IDF tranche 10000",
        labels={"DEC_MED18": "Salaire Médian (€)"},
        nbins=30,
    )

    fig.update_layout(
        title={
            "text": "",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 20, "family": "Arial, sans-serif", "color": "#2c3e50"},
        },
        bargap=0.1,
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

    # Composant HTML contenant le graphique
    return html.Div(
        children=[
            html.H3(
                "Nombre de Villes par Intervalle de Salaires Médians en IDF tranche de 10K",
                style={
                    "text-align": "center",
                    "color": "#2c3e50",
                    "margin-bottom": "20px",
                },
            ),
            dcc.Graph(figure=fig),
            html.H4(
                "La majorité des villes présentent un salaire médian compris entre 20 000€ et 30 000€.",
                style={
                    "text-align": "center",
                    "color": "#2c3e50",
                    "margin-bottom": "20px",
                },
            ),

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

