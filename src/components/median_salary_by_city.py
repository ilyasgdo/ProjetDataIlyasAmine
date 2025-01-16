"""Module pour la visualisation des salaires médians et de l'indice de Gini."""

from dash import html, dcc
import plotly.express as px
import pandas as pd
import os
from typing import Tuple
from utils.normalise_name import normalize_name
import dash_bootstrap_components as dbc

# Chemins vers les fichiers de données
CLEANED_DATA_PATH_SALAIRE = os.path.join("data", "cleaned", "cleanedsalaire.xlsx")
CLEANED_DATA_PATH_COMMUNES_IDF = os.path.join(
    "data", "cleaned", "cleanedcommunesiledefrance.xlsx"
)

# Charger la liste des villes à partir du fichier Excel
villes_idf_df = pd.read_excel(CLEANED_DATA_PATH_COMMUNES_IDF)
villes_idf = villes_idf_df.iloc[:, 0].apply(normalize_name).tolist()

# Charger le fichier des statistiques à partir d'Excel
df_salaire = pd.read_excel(CLEANED_DATA_PATH_SALAIRE)

# Ajouter une colonne normalisée pour la comparaison
df_salaire["LIBCOM_normalized"] = df_salaire["LIBCOM"].apply(normalize_name)

# Filtrer les lignes où la colonne normalisée est dans la liste des villes d'Île-de-France
df_filtre_idf = df_salaire[df_salaire["LIBCOM_normalized"].isin(villes_idf)]

# Trier les résultats par la colonne d'origine 'LIBCOM'
df_filtre_idf = df_filtre_idf.sort_values(by="LIBCOM")

# Liste unique des villes disponibles dans la colonne LIBCOM
villes = df_filtre_idf["LIBCOM"].unique()


def create_graph_layout(df_filtre: pd.DataFrame) -> html.Div:
    """
    Crée la mise en page avec le Dropdown et le graphique.

    Args:
        df_filtre (pd.DataFrame): DataFrame contenant les données filtrées.

    Returns:
        html.Div: Un composant Dash contenant le titre, le dropdown et le graphique.
    """
    villes = df_filtre["LIBCOM"].unique()
    return dbc.Container(
        children=[
            dbc.Row(
                dbc.Col(
                    html.H1(
                        "Visualisation des Salaires Médians et Indice de Gini",
                        className="text-center my-4",
                    ),
                ),
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        "Sélectionnez une ville pour afficher le graphique et les informations associées",
                        className="text-center mb-4",
                    ),
                ),
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(
                        id="ville-selector",
                        options=[{"label": ville, "value": ville} for ville in sorted(villes)],
                        value=villes[0],  # Valeur par défaut (première ville de la liste)
                        placeholder="Choisissez une ville",
                        className="mb-4",
                    ),
                    width={"size": 6, "offset": 3},
                ),
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id="salaire-gini-graph"),
                ),
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(
                        id="iris-info",
                        className="mt-4 p-3 bg-light border rounded",
                        style={"fontWeight": "bold"},
                    ),
                ),
            ),
        ],
        fluid=True,
    )


def update_graph(selected_ville: str) -> Tuple[px.bar, html.Div]:
    """
    Met à jour le graphique et les informations associées à la ville sélectionnée.

    Args:
        selected_ville (str): La ville sélectionnée dans le dropdown.

    Returns:
        Tuple[px.bar, html.Div]: Un tuple contenant la figure Plotly et les informations textuelles.
    """
    # Filtrer les données pour la ville sélectionnée
    filtered_df = df_filtre_idf[df_filtre_idf["LIBCOM"] == selected_ville]

    # Trier les données par salaire médian de manière décroissante
    filtered_df = filtered_df.sort_values(by="DEC_MED18", ascending=False)

    # Ajouter une colonne texte pour afficher les parts sur chaque barre
    filtered_df["text_info"] = (
        "Part chômage: "
        + filtered_df["DEC_PCHO18"].astype(str)
        + "%<br>"
        + "Part non salarié: "
        + filtered_df["DEC_PBEN18"].astype(str)
        + "%<br>"
        + "Part pensions/retraites: "
        + filtered_df["DEC_PPEN18"].astype(str)
        + "%<br>"
    )

    # Identifier les IRIS pour chaque critère
    iris_chomage = filtered_df.loc[filtered_df["DEC_PCHO18"].idxmax(), "LIBIRIS"]
    iris_gini = filtered_df.loc[filtered_df["DEC_GI18"].idxmax(), "LIBIRIS"]
    iris_retraites = filtered_df.loc[filtered_df["DEC_PPEN18"].idxmax(), "LIBIRIS"]

    # Créer le texte explicatif
    iris_info = html.Div(
        children=[
            html.P(f"IRIS avec le taux de chômage le plus élevé : {iris_chomage}"),
            html.P(f"IRIS avec l'indice de Gini le plus élevé : {iris_gini}"),
            html.P(f"IRIS avec la plus grande part de retraités : {iris_retraites}"),
        ]
    )

    # Créer  graphique 
    fig = px.bar(
        filtered_df,
        x="LIBIRIS",  # IRIS
        y="DEC_MED18",  # Salaire médian
        color="DEC_GI18",  # Indice de Gini pour la couleur
        title=f"Salaire médian et Indice de Gini pour {selected_ville}",
        labels={
            "LIBIRIS": "Libellé IRIS",
            "DEC_MED18": "Salaire Médian (€)",
            "DEC_GI18": "Indice de Gini",
        },
        color_continuous_scale="Viridis", 
        text="text_info",  
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(yaxis=dict(range=[0, 80000]))

    return fig, iris_info