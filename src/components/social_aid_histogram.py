# src/components/social_aid_histogram.py
import plotly.express as px
from dash import html, dcc

def create_social_aid_histogram(df):
    # Créer un DataFrame pour les parts de chômage et de retraités
    df_social_aid = df[["LIBCOM", "DEC_PCHO18", "DEC_PPEN18"]]
    
    # Création du graphique
    fig = px.bar(
        df_social_aid,
        x="LIBCOM",
        y=["DEC_PCHO18", "DEC_PPEN18"],
        title="Parts d'Aide Sociale : Chômage vs Retraite par Ville",
        labels={
            "LIBCOM": "Ville",
            "DEC_PCHO18": "Part Chômage (%)",
            "DEC_PPEN18": "Part Retraités (%)"
        },
        barmode="group",  # Afficher les barres côte à côte
        height=600
    )
    
    # Personnalisation du graphique (si nécessaire)
    fig.update_layout(
        xaxis_title="Ville",
        yaxis_title="Pourcentage (%)",
        xaxis_tickangle=-45  # Incliner les noms des villes pour une meilleure lisibilité
    )
    
    # Retourner le graphique dans un composant HTML
    return html.Div([
        html.H3("Histogramme des Parts d'Aide Sociale : Chômage et Retraités"),
        dcc.Graph(figure=fig)
    ])
