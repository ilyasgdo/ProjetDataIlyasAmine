from dash import html, dcc
import plotly.express as px
import pandas as pd
import os
from utils.normalise_name import normalize_name

# Chemin vers le fichier de données
CLEANED_DATA_PATH = os.path.join("data", "cleaned", "cleanedsalaire.xlsx")

CLEANED_DATA_PATH_SALAIRE = os.path.join("data", "cleaned", "cleanedsalaire.xlsx")
CLEANED_DATA_PATH_COMMUNES_IDF = os.path.join(
    "data/cleaned", "cleanedcommunesiledefrance.xlsx"
)

# Charger la liste des villes à partir du fichier Excel
villes_idf_df = pd.read_excel(CLEANED_DATA_PATH_COMMUNES_IDF)
villes_idf = (
    villes_idf_df.iloc[:, 0].apply(normalize_name).tolist()
)  # Normaliser les noms de villes

# Charger le fichier des statistiques à partir d'Excel
df_salaire = pd.read_excel(CLEANED_DATA_PATH_SALAIRE)

# Ajouter une colonne normalisée pour la comparaison
df_salaire["LIBCOM_normalized"] = df_salaire["LIBCOM"].apply(normalize_name)

# Filtrer les lignes où la colonne normalisée est dans la liste des villes d'Île-de-France
df_filtre_IDF = df_salaire[df_salaire["LIBCOM_normalized"].isin(villes_idf)]

# Trier les résultats par la colonne d'origine 'LIBCOM'
df_filtre_IDF = df_filtre_IDF.sort_values(by="LIBCOM")

# Liste unique des villes disponibles dans la colonne LIBCOM
villes = df_filtre_IDF["LIBCOM"].unique()


def create_graph_layout(df_filtre):
    villes = df_filtre["LIBCOM"].unique()
    print(villes)
    """Retourne la mise en page avec le Dropdown et le graphique."""
    return html.Div(
        children=[
            html.H1(children="Visualisation des Salaires Médians et Indice de Gini"),
            html.Div(
                children="Sélectionnez une ville pour afficher le graphique et les informations associées."
            ),
            # Dropdown pour sélectionner la ville
            dcc.Dropdown(
                id="ville-selector",
                options=[{"label": ville, "value": ville} for ville in sorted(villes)],
                value=villes[0],  # Valeur par défaut (première ville de la liste)
                placeholder="Choisissez une ville",
            ),
            dcc.Graph(id="salaire-gini-graph"),
            # Texte pour afficher les IRIS avec des valeurs extrêmes
            html.Div(id="iris-info", style={"marginTop": "20px", "fontWeight": "bold"}),
        ]
    )


def update_graph(selected_ville):
    """Met à jour le graphique et les informations associées à la ville sélectionnée."""
    # Filtrer les données pour la ville sélectionnée
    filtered_df = df_filtre_IDF[df_filtre_IDF["LIBCOM"] == selected_ville]

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
            "DEC_GI18": "Indice de Gini",
        },
        color_continuous_scale="Viridis",  # Palette de couleurs
        text="text_info",  # Texte à afficher sur les barres
    )

    # Ajuster l'apparence pour que le texte soit affiché sur les barres
    fig.update_traces(textposition="outside")
    

    # Définir les limites de l'axe x (salaire médian) entre 0 et 80 000
    fig.update_layout(
        yaxis=dict(
            range=[0, 80000]  # Limite de l'axe x entre 0 et 80000
        )
    )

    return fig, iris_info
