import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output

def create_pie_chart_component(app, data: pd.DataFrame) -> html.Div:
    """
    Crée un composant contenant un sélecteur de ville stylisé et un diagramme circulaire,
    basé sur les parts des différentes sources de revenus.
    
    Args:
        app (Dash): L'application Dash.
        data (pd.DataFrame): Les données filtrées contenant les informations des villes.
    
    Returns:
        html.Div: Le composant contenant le sélecteur et le graphique.
    """
    # Normaliser les noms de colonnes pour éviter les erreurs de casse
    data["LIBCOM_normalized"] = data["LIBCOM"].str.lower()

    # Liste des villes disponibles
    villes = data["LIBCOM_normalized"].unique()

    # Ville par défaut (Bussy-Saint-Georges)
    ville_par_defaut = "bussy-saint-georges"

    # Vérifier que la ville par défaut est présente dans les données
    if ville_par_defaut not in villes:
        raise ValueError(f"La ville par défaut '{ville_par_defaut}' n'est pas présente dans les données.")

    # Conteneur du composant
    layout = html.Div(
        children=[
            html.Div(
                children=[
                    html.H2(
                        "Répartition des sources de revenus",
                        style={
                            "text-align": "center",
                            "color": "#2c3e50",
                            "font-family": "Arial, sans-serif",
                            "margin-bottom": "20px",
                        },
                    ),
                    html.P(
                        "Sélectionnez une ville dans la liste déroulante pour afficher les données correspondantes.",
                        style={
                            "text-align": "center",
                            "color": "#34495e",
                            "font-size": "16px",
                            "font-family": "Arial, sans-serif",
                            "margin-bottom": "20px",
                        },
                    ),
                    # Sélecteur de ville
                    dcc.Dropdown(
                        id="ville-selector2",
                        options=[{"label": ville.title(), "value": ville} for ville in villes],
                        value=ville_par_defaut,  # Définir la ville par défaut
                        placeholder="Sélectionnez une ville...",
                        style={
                            "width": "60%",
                            "margin": "0 auto 20px auto",
                            "font-family": "Arial, sans-serif",
                            "font-size": "14px",
                        },
                    ),
                ],
                style={
                    "padding": "20px",
                    "background-color": "#ecf0f1",
                    "border-radius": "10px",
                    "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                },
            ),
            # Conteneur pour le graphique
            html.Div(id="pie-chart-container"),
        ],
        style={"max-width": "800px", "margin": "0 auto", "padding": "20px"},
    )

    # Callback pour mettre à jour le graphique en fonction de la ville sélectionnée
    @app.callback(
        Output("pie-chart-container", "children"),
        [Input("ville-selector2", "value")],
    )
    def update_pie_chart(selected_city):
        if not selected_city:
            return html.Div(
                "Veuillez sélectionner une ville.",
                style={
                    "text-align": "center",
                    "color": "#e74c3c",
                    "margin-top": "20px",
                    "font-size": "18px",
                    "font-family": "Arial, sans-serif",
                },
            )

        # Filtrer les données pour la ville sélectionnée
        city_data = data[data["LIBCOM_normalized"] == selected_city]

        # Vérifier qu'il y a des données pour la ville sélectionnée
        if city_data.empty:
            return html.Div(
                f"Aucune donnée disponible pour la ville sélectionnée : {selected_city.title()}",
                style={
                    "text-align": "center",
                    "color": "#e74c3c",
                    "margin-top": "20px",
                    "font-size": "18px",
                    "font-family": "Arial, sans-serif",
                },
            )

        # Colonnes représentant les parts des différentes sources de revenus
        revenue_categories = {
            "Part des salaires et traitements": "DEC_PTSA18",
            "Part des indemnités de chômage": "DEC_PCHO18",
            "Part des activités non salariées": "DEC_PBEN18",
            "Part des pensions, retraites et rentes": "DEC_PPEN18",
            "Part des autres revenus": "DEC_PAUT18",
        }

        # Extraire les valeurs des catégories
        values = city_data[list(revenue_categories.values())].iloc[0]

        # Vérifier que les valeurs ne sont pas nulles ou manquantes
        if values.isnull().any():
            return html.Div(
                "Les données pour les catégories sélectionnées sont incomplètes.",
                style={
                    "text-align": "center",
                    "color": "#e74c3c",
                    "margin-top": "20px",
                    "font-size": "18px",
                    "font-family": "Arial, sans-serif",
                },
            )

        # Créer le diagramme circulaire avec Plotly
        fig = px.pie(
            values=values,
            names=list(revenue_categories.keys()),
            title=f"Répartition des revenus pour la ville : {selected_city.title()}",
            color_discrete_sequence=px.colors.sequential.Tealgrn,
        )

        # Ajouter un style au titre du graphique
        fig.update_layout(
            title_font=dict(size=20, family="Arial, sans-serif", color="#2c3e50"),
            margin=dict(l=40, r=40, t=60, b=40),
        )

        return dcc.Graph(figure=fig)

    return layout