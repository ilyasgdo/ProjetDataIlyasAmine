from dash import Dash, html, Input, Output, dcc  # Ajout de dcc pour les filtres
import pandas as pd
import os
import re

from src.components.graph1 import create_graph_layout, update_graph
from src.components.header import create_header
from src.components.navbar import create_navbar
from src.components.footer import create_footer
from src.components.histogram import create_histogram
from src.components.social_aid_histogram import create_social_aid_histogram
from src.components.histogram_salary_range import create_histogram_by_salary_range
from src.components.bar_chart import generate_bar_chart
from src.components.scatter_plot import generate_scatter_plot
from src.components.line_chart import generate_line_chart
from src.components.heatmap import generate_heatmap
from src.components.filters import generate_filters
from utils.get_data import download_all_data
from utils.clean_data import clean_all_raw_files
from utils.normalise_name import normalize_name


# Chemin vers le fichier Excel contenant les données
CLEANED_DATA_PATH_SALAIRE = os.path.join("data", "cleaned", "cleanedsalaire.xlsx")
CLEANED_DATA_PATH_COMMUNES_IDF = os.path.join(
    "data/cleaned", "cleanedcommunesiledefrance.xlsx"
)

# telecharge les données si elles ne sont pas présentes
download_all_data()

# nettoye tout les fichiers brut si ils ne sont pas présents dans cleaned
clean_all_raw_files()


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

# Supprimer la colonne temporaire avant affichage ou sauvegarde
CLEANED_DATA_PATH_SALAIRE = os.path.join("data", "cleaned", "temp.xlsx")

# Afficher le résultat
df_filtre_IDF.to_excel(CLEANED_DATA_PATH_SALAIRE, index=False)


# Charger les données à partir du fichier Excel


# Initialisation de l'application Dash
app = Dash(__name__)

# Définir la mise en page de l'application
app.layout = html.Div(
    children=[
        create_header(),  # Ajouter le Header
        create_navbar(),  # Ajouter la Navbar
        # Ajout des filtres
        generate_filters(df_filtre_IDF),
        # Conteneur pour les graphiques
        html.Div(id="graph-container"),
        # Ajouter des graphiques statiques
        create_histogram(df_filtre_IDF),  # Histogramme des salaires médians
        create_social_aid_histogram(
            df_filtre_IDF
        ),  # Graphique circulaire de l'indice de Gini
        create_histogram_by_salary_range(
            df_filtre_IDF
        ),  # Histogramme par intervalle de salaires
        create_graph_layout(df_filtre_IDF),  # Graphique de base
        generate_heatmap(df_filtre_IDF),
        generate_line_chart(df_filtre_IDF),
        create_footer(),  # Ajouter le Footer
    ]
)


# Callback pour mettre à jour les graphiques en fonction des sélections
@app.callback(
    Output("graph-container", "children"),
    [Input("region-selector", "value"), Input("data-type-selector", "value")],
)
def update_graphs(selected_region, selected_data_type):
    # Filtrer les données en fonction de la région sélectionnée
    filtered_df = (
        df_filtre_IDF
        if not selected_region
        else df_filtre_IDF[df_filtre_IDF["LIBCOM"] == selected_region]
    )

    # Générer les graphiques en fonction du type de données sélectionné
    bar_chart = generate_bar_chart(filtered_df, selected_data_type)
    scatter_plot = generate_scatter_plot(filtered_df, "DEC_MED18", "DEC_GI18")
    line_chart = generate_line_chart(filtered_df, selected_data_type)
    heatmap = generate_heatmap(filtered_df, selected_data_type)

    # Retourner les graphiques
    return html.Div([bar_chart, scatter_plot, line_chart, heatmap])


# Callback pour mettre à jour le graphique et les textes
app.callback(
    [Output("salaire-gini-graph", "figure"), Output("iris-info", "children")],
    [Input("ville-selector", "value")],
)(update_graph)

if __name__ == "__main__":
    app.run(host="localhost", port=7999, debug=True)
