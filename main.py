from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import os

app = Dash(
    __name__,
    # Ajout des balises meta et autres dans l'en-tête
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)

# Chemin vers le fichier de données
CLEANED_DATA_PATH = os.path.join("data", "cleaned", "cleanedsalaire.xlsx")
# Lecture des données Excel
df = pd.read_excel(CLEANED_DATA_PATH)

# Liste unique des villes disponibles dans la colonne LIBCOM
villes = df["LIBCOM"].unique()

# Layout de l'application
app.layout = html.Div(children=[
    # En-tête de la page HTML (balises <head>)
    html.Header([
        html.Title("Visualisation des Salaires Médians et Indice de Gini"),  # Titre de la page
        html.Meta(name="description", content="Visualisation des salaires médians et indices de Gini pour différentes villes."),
        html.Meta(name="author", content="Ilyas Ghandaoui"),
        html.Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"),  # Exemple de lien vers un CSS externe
        # Vous pouvez ajouter d'autres balises comme des feuilles de style internes si nécessaire
    ]),
    
    html.H1(children="Visualisation des Salaires Médians et Indice de Gini"),

    html.Div(children='''Sélectionnez une ville pour afficher le graphique correspondant.'''),

    # Dropdown pour sélectionner la ville
    dcc.Dropdown(
        id='ville-selector',
        options=[{'label': ville, 'value': ville} for ville in sorted(villes)],
        value=villes[0],  # Valeur par défaut (première ville de la liste)
        placeholder="Choisissez une ville"
    ),

    dcc.Graph(
        id='salaire-gini-graph'
    )
])

# Callback pour mettre à jour le graphique en fonction de la ville sélectionnée
@app.callback(
    Output('salaire-gini-graph', 'figure'),
    Input('ville-selector', 'value')
)
def update_graph(selected_ville):
    # Filtrer les données pour la ville sélectionnée
    filtered_df = df[df["LIBCOM"] == selected_ville]

    # Trier les données par salaire médian de manière décroissante
    filtered_df = filtered_df.sort_values(by="DEC_MED18", ascending=False)

    # Créer un graphique pour les salaires médians et l'indice de Gini
    fig = px.bar(
        filtered_df,
        x="LIBIRIS",  # Libellé de l'IRIS
        y="DEC_MED18",  # Salaire médian
        color="DEC_GI18",  # Indice de Gini représenté par la couleur
        title=f"Salaire médian et Indice de Gini pour {selected_ville}",
        labels={"LIBIRIS": "Libellé IRIS", "DEC_MED18": "Salaire Médian (€)", "DEC_GI18": "Indice de Gini"},
        color_continuous_scale="Viridis"  # Palette de couleurs
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
