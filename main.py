from dash import Dash, html, Input, Output, dcc  # Ajout de dcc pour les filtres
import pandas as pd
import os
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


# Chemin vers le fichier Excel contenant les données
CLEANED_DATA_PATH = os.path.join("data", "cleaned", "cleanedsalaire.xlsx")

# Charger les données à partir du fichier Excel
df = pd.read_excel(CLEANED_DATA_PATH)

#telecharge les données si elles ne sont pas présentes
download_all_data()

#nettoye tout les fichiers brut si ils ne sont pas présents dans cleaned
clean_all_raw_files()

# Initialisation de l'application Dash
app = Dash(__name__)

# Définir la mise en page de l'application
app.layout = html.Div(children=[
    create_header(),  # Ajouter le Header
    create_navbar(),  # Ajouter la Navbar
    
    # Ajout des filtres
    generate_filters(df),

    # Conteneur pour les graphiques
    html.Div(id="graph-container"),

    # Ajouter des graphiques statiques
    create_histogram(df),  # Histogramme des salaires médians
    create_social_aid_histogram(df),  # Graphique circulaire de l'indice de Gini
    create_histogram_by_salary_range(df),  # Histogramme par intervalle de salaires
    create_graph_layout(df),  # Graphique de base
    generate_heatmap(df),
    generate_line_chart(df),
    create_footer(),  # Ajouter le Footer

])

# Callback pour mettre à jour les graphiques en fonction des sélections
@app.callback(
    Output("graph-container", "children"),
    [Input("region-selector", "value"),
     Input("data-type-selector", "value")]
)
def update_graphs(selected_region, selected_data_type):
    # Filtrer les données en fonction de la région sélectionnée
    filtered_df = df if not selected_region else df[df["LIBCOM"] == selected_region]

    # Générer les graphiques en fonction du type de données sélectionné
    bar_chart = generate_bar_chart(filtered_df, selected_data_type)
    scatter_plot = generate_scatter_plot(filtered_df, "DEC_MED18", "DEC_GI18")
    line_chart = generate_line_chart(filtered_df, selected_data_type)
    heatmap = generate_heatmap(filtered_df, selected_data_type)

    # Retourner les graphiques
    return html.Div([
        bar_chart,
        scatter_plot,
        line_chart,
        heatmap
    ])

# Callback pour mettre à jour le graphique et les textes
app.callback(
    [Output('salaire-gini-graph', 'figure'),
     Output('iris-info', 'children')],
    [Input('ville-selector', 'value')]
)(update_graph)

if __name__ == '__main__':
    app.run(debug=True)
