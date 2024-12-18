from dash import Dash, html  # Ajout de l'importation de html
import pandas as pd
import os
from src.components.graph1 import create_graph_layout, update_graph
from src.components.header import create_header
from src.components.navbar import create_navbar
from src.components.footer import create_footer
from src.components.histogram import create_histogram
from src.components.social_aid_histogram import  create_social_aid_histogram
from src.components.histogram_salary_range import create_histogram_by_salary_range

from dash import Input, Output

CLEANED_DATA_PATH = os.path.join("data", "cleaned", "cleanedsalaire.xlsx")

# Charger les données à partir du fichier Excel
df = pd.read_excel(CLEANED_DATA_PATH)

# Initialisation de l'application Dash
app = Dash(__name__)

# Définir la mise en page de l'application
app.layout = html.Div(children=[
    create_header(),  # Ajouter le Header
    create_navbar(),  # Ajouter la Navbar
    create_histogram(df),  # Ajouter l'histogramme des salaires médians
    create_social_aid_histogram(df),  # Ajouter le graphique circulaire de l'indice de Gini
    create_histogram_by_salary_range(df),  # Ajouter l'histogramme par intervalle de salaires
    create_graph_layout(df),  # Ajouter le graphique
    create_footer()  # Ajouter le Footer
])

# Callback pour mettre à jour le graphique et les textes
app.callback(
    [Output('salaire-gini-graph', 'figure'),
     Output('iris-info', 'children')],
    [Input('ville-selector', 'value')]
)(update_graph)

if __name__ == '__main__':
    app.run(debug=True)
