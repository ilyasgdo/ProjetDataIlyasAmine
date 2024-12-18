from dash import html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import os

# Chemin vers le fichier de données
CLEANED_DATA_PATH = os.path.join("data", "cleaned", "cleanedsalaire.xlsx")

# Lecture des données Excel
df = pd.read_excel(CLEANED_DATA_PATH)

# Liste unique des villes disponibles dans la colonne LIBCOM
villes = df["LIBCOM"].unique()

def create_graph_layout(df):
    villes = df["LIBCOM"].unique()
    """Retourne la mise en page avec le Dropdown et le graphique."""
    return html.Div(children=[
        html.H1(children="Visualisation des Salaires Médians et Indice de Gini"),
        html.Div(children="Sélectionnez une ville pour afficher le graphique et les informations associées."),
        
        # Dropdown pour sélectionner la ville
        dcc.Dropdown(
            id='ville-selector',
            options=[{'label': ville, 'value': ville} for ville in sorted(villes)],
            value=villes[0],  # Valeur par défaut (première ville de la liste)
            placeholder="Choisissez une ville"
        ),

        dcc.Graph(
            id='salaire-gini-graph'
        ),

        # Texte pour afficher les IRIS avec des valeurs extrêmes
        html.Div(id='iris-info', style={'marginTop': '20px', 'fontWeight': 'bold'})
    ])

def update_graph(selected_ville):
    """Met à jour le graphique et les informations associées à la ville sélectionnée."""
    # Filtrer les données pour la ville sélectionnée
    filtered_df = df[df["LIBCOM"] == selected_ville]

    # Trier les données par salaire médian de manière décroissante
    filtered_df = filtered_df.sort_values(by="DEC_MED18", ascending=False)

    # Ajouter une colonne texte pour afficher les parts sur chaque barre
    filtered_df["text_info"] = (
        "Part chômage: " + filtered_df["DEC_PCHO18"].astype(str) + "%<br>" +
        "Part non salarié: " + filtered_df["DEC_PBEN18"].astype(str) + "%<br>" +
        "Part pensions/retraites: " + filtered_df["DEC_PPEN18"].astype(str) + "%<br>"
    )

    # Identifier les IRIS pour chaque critère
    iris_chomage = filtered_df.loc[filtered_df["DEC_PCHO18"].idxmax(), "LIBIRIS"]
    iris_gini = filtered_df.loc[filtered_df["DEC_GI18"].idxmax(), "LIBIRIS"]
    iris_retraites = filtered_df.loc[filtered_df["DEC_PPEN18"].idxmax(), "LIBIRIS"]

    # Créer le texte explicatif
    iris_info = html.Div(children=[
        html.P(f"IRIS avec le taux de chômage le plus élevé : {iris_chomage}"),
        html.P(f"IRIS avec l'indice de Gini le plus élevé : {iris_gini}"),
        html.P(f"IRIS avec la plus grande part de retraités : {iris_retraites}")
    ])

    # Créer un graphique pour les salaires médians et l'indice de Gini
    fig = px.bar(
        filtered_df,
        x="LIBIRIS",  # Libellé de l'IRIS
        y="DEC_MED18",  # Salaire médian
        color="DEC_GI18",  # Indice de Gini représenté par la couleur
        title=f"Salaire médian et Indice de Gini pour {selected_ville}",
        labels={
            "LIBIRIS": "Libellé IRIS",
            "DEC_MED18": "Salaire Médian (€)",
            "DEC_GI18": "Indice de Gini"
        },
        color_continuous_scale="Viridis",  # Palette de couleurs
        text="text_info"  # Texte à afficher sur les barres
    )

    # Ajuster l'apparence pour que le texte soit affiché sur les barres
    fig.update_traces(textposition='outside')

    return fig, iris_info
