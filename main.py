from typing import Optional
from dash import Dash, html, Input, Output, dcc
import dash_bootstrap_components as dbc  
import pandas as pd
import os

from src.components.median_salary_by_city import create_graph_layout, update_graph
from src.components.header import create_header
from src.components.navbar import create_navbar
from src.components.footer import create_footer
from src.components.histogram import create_histogram
from src.components.social_aid_histogram import create_social_aid_histogram
from src.components.histogram_salary_range import create_histogram_by_salary_range
from src.components.heatmap import generate_heatmap
from src.components.pie_chart import create_pie_chart_component
from utils.get_data import download_all_data
from utils.clean_data import clean_all_raw_files
from utils.normalise_name import normalize_name

# --- Configuration des chemins vers les fichiers ---

CLEANED_DATA_PATH_SALAIRE = os.path.join("data", "cleaned", "cleanedsalaire.xlsx")
CLEANED_DATA_PATH_COMMUNES_IDF = os.path.join(
    "data", "cleaned", "cleanedcommunesiledefrance.xlsx"
)

# --- Téléchargement et nettoyage des données si nécessaire ---
download_all_data()
clean_all_raw_files()

# --- Chargement et filtrage des données ---

# Charger la liste des villes et normaliser leurs noms
villes_idf_df = pd.read_excel(CLEANED_DATA_PATH_COMMUNES_IDF)
villes_idf = villes_idf_df.iloc[:, 0].apply(normalize_name).tolist()

# Charger les données salariales et filtrer les communes de l'Île-de-France
df_salaire = pd.read_excel(CLEANED_DATA_PATH_SALAIRE)
df_salaire["LIBCOM_normalized"] = df_salaire["LIBCOM"].apply(normalize_name)
df_filtre_IDF = df_salaire[df_salaire["LIBCOM_normalized"].isin(villes_idf)].sort_values(by="LIBCOM")
df_filtre_IDF = df_filtre_IDF.drop(columns=["LIBCOM_normalized"])

# --- Initialisation de l'application Dash avec Bootstrap ---
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# --- Mise en page principale de l'application ---
app.layout = dbc.Container(
    fluid=True,
    children=[
        create_header(),
        create_navbar(),
        dbc.Container(
            fluid=False,
            children=[
                create_pie_chart_component(app, df_filtre_IDF),  # Graphique circulaire
                dbc.Row(
                    [
                        # Première rangée : Histogramme et graphique d'aide sociale
                        dbc.Col(create_histogram(df_filtre_IDF), width=6, className="mb-4"),
                        dbc.Col(create_social_aid_histogram(df_filtre_IDF), width=6, className="mb-4"),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        # Deuxième rangée : Histogramme par salaires et carte thermique
                        dbc.Col(create_histogram_by_salary_range(df_filtre_IDF), width=6, className="mb-4"),
                        dbc.Col(generate_heatmap(df_filtre_IDF), width=6, className="mb-4"),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    dbc.Col(create_graph_layout(df_filtre_IDF), width=12, className="mb-4"),
                ),
            ],
            style={
                "backgroundColor": "#f4f4f4",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
            },
        ),
        create_footer(),  # Pied de page
    ],
    style={"fontFamily": "Arial, sans-serif", "paddingTop": "20px"},
)

# --- Callback pour mettre à jour le graphique et les textes ---
@app.callback(
    [Output("salaire-gini-graph", "figure"), Output("iris-info", "children")],
    [Input("ville-selector", "value")],
)
def update_callback(ville: Optional[str]) -> tuple:
    """
    Met à jour le graphique et les informations textuelles en fonction de la ville sélectionnée.

    Args:
        ville (Optional[str]): La ville sélectionnée dans le menu déroulant.

    Returns:
        tuple: Le graphique mis à jour et le texte d'informations.
    """
    return update_graph(ville)


# --- Exécution de l'application ---
if __name__ == "__main__":
    app.run(host="localhost", port=7999, debug=True)
