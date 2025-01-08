from typing import Optional
from dash import Dash, html, Input, Output, dcc
import pandas as pd
import os

from src.components.graph1 import create_graph_layout, update_graph
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

# --- Définition des chemins vers les fichiers ---

CLEANED_DATA_PATH_SALAIRE = os.path.join("data", "cleaned", "cleanedsalaire.xlsx")
CLEANED_DATA_PATH_COMMUNES_IDF = os.path.join(
    "data", "cleaned", "cleanedcommunesiledefrance.xlsx"
)

# --- Téléchargement et nettoyage des données si nécessaire ---

download_all_data()
clean_all_raw_files()

# --- Chargement et filtrage des données ---

villes_idf_df = pd.read_excel(CLEANED_DATA_PATH_COMMUNES_IDF)
villes_idf = (
    villes_idf_df.iloc[:, 0].apply(normalize_name).tolist()
)

df_salaire = pd.read_excel(CLEANED_DATA_PATH_SALAIRE)
df_salaire["LIBCOM_normalized"] = df_salaire["LIBCOM"].apply(normalize_name)
df_filtre_IDF = df_salaire[df_salaire["LIBCOM_normalized"].isin(villes_idf)].sort_values(by="LIBCOM")
df_filtre_IDF = df_filtre_IDF.drop(columns=["LIBCOM_normalized"])

# --- Initialisation de l'application Dash ---

app = Dash(__name__)

# --- Définir la mise en page de l'application ---

app.layout = html.Div(
    children=[
        create_header(),
        create_navbar(),
        html.Div(
            children=[
                create_pie_chart_component(app, df_filtre_IDF),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                create_histogram(df_filtre_IDF),
                                create_social_aid_histogram(df_filtre_IDF),
                            ],
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "gap": "20px",
                                "marginBottom": "20px",
                            },
                        ),
                        html.Div(
                            children=[
                                create_histogram_by_salary_range(df_filtre_IDF),
                                generate_heatmap(df_filtre_IDF),
                            ],
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "gap": "20px",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "width": "100%",
                    },
                ),
                create_graph_layout(df_filtre_IDF),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "backgroundColor": "#f4f4f4",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                "maxWidth": "1200px",
                "margin": "0 auto",
            },
        ),
        create_footer(),
    ],
    style={
        "fontFamily": "Arial, sans-serif",
        "padding": "20px",
        "backgroundColor": "#ffffff",
    },
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
