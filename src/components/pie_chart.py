import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash import Dash


def create_pie_chart_component(app: Dash, data: pd.DataFrame) -> html.Div:
    """
    Crée un composant Dash contenant un sélecteur de ville et un diagramme circulaire
    affichant la répartition des sources de revenus pour une ville donnée.

    Args:
        app (Dash): L'application Dash pour les callbacks.
        data (pd.DataFrame): Données filtrées contenant les informations des villes.

    Returns:
        html.Div: Un composant contenant un sélecteur de ville et un graphique interactif.
    """
    # Normaliser les noms des villes pour éviter les erreurs
    data["LIBCOM_normalized"] = data["LIBCOM"].str.lower()

    # Liste des villes disponibles
    villes = sorted(data["LIBCOM_normalized"].unique())

    # ville par défaut
    ville_par_defaut = "bussy-saint-georges"

    if ville_par_defaut not in villes:
        raise ValueError(f"La ville par défaut '{ville_par_defaut}' n'existe pas dans les données.")

    # Mise en page du composant
    layout = dbc.Container(
        fluid=True,
        children=[
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H2(
                                "Répartition des Sources de Revenus",
                                className="card-title text-center text-primary",
                            ),
                            html.P(
                                "Sélectionnez une ville pour afficher les données correspondantes.",
                                className="text-center text-muted",
                            ),
                            dcc.Dropdown(
                                id="ville-selector2",
                                options=[
                                    {"label": ville.title(), "value": ville} for ville in villes
                                ],
                                value=ville_par_defaut,
                                placeholder="Sélectionnez une ville...",
                                className="mb-4",
                            ),
                        ]
                    )
                ],
                className="shadow-sm mb-4",
            ),
            dbc.Row(
                dbc.Col(html.Div(id="pie-chart-container")),
                className="mb-4",
            ),
        ],
    )

    # Callback pour mettre à jour le graphique
    @app.callback(
        Output("pie-chart-container", "children"),
        [Input("ville-selector2", "value")],
    )
    def update_pie_chart(selected_city: str) -> html.Div:
        """Met à jour le graphique en fonction de la ville sélectionnée."""
        if not selected_city:
            return html.Div(
                "Veuillez sélectionner une ville.",
                className="text-center text-danger mt-3",
            )

        # Filtrer les données pour la ville sélectionnée
        city_data = data[data["LIBCOM_normalized"] == selected_city]

        if city_data.empty:
            return html.Div(
                f"Aucune donnée disponible pour la ville sélectionnée : {selected_city.title()}",
                className="text-center text-warning mt-3",
            )

        # Définir les catégories et les colonnes correspondantes
        revenue_categories = {
            "Salaires et traitements": "DEC_PTSA18",
            "Indemnités de chômage": "DEC_PCHO18",
            "Activités non salariées": "DEC_PBEN18",
            "Pensions, retraites et rentes": "DEC_PPEN18",
            "Autres revenus": "DEC_PAUT18",
        }

        # Extraire les données de la ville pour les catégories
        values = city_data[list(revenue_categories.values())].iloc[0]

        if values.isnull().any():
            return html.Div(
                "Les données pour cette ville sont incompltes.",
                className="text-center text-danger mt-3",
            )

        # Créer le graphique 
        fig = px.pie(
            values=values,
            names=list(revenue_categories.keys()),
            title=f"Répartition des revenus pour {selected_city.title()}",
            color_discrete_sequence=px.colors.sequential.Agsunset_r,
        )

        # Mise en forme du graphique
        fig.update_layout(
            title_font=dict(size=20, family="Arial, sans-serif", color="#2c3e50"),
            margin=dict(l=20, r=20, t=50, b=20),
        )

        return dcc.Graph(figure=fig)

    return layout
