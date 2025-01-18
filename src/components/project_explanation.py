from dash import html
import dash_bootstrap_components as dbc

def create_project_explanation_component() -> dbc.Card:
    """
    Crée un composant qui explique le projet, les données utilisées, les outils et les limites.

    Returns:
        dbc.Card: Un composant Dash Bootstrap contenant une explication du projet.
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H3("À propos de ce projet", className="card-title"),
                html.P(
                    "Ce projet vise à visualiser les revenus déclarés des Français en 2018, en utilisant des données provenant de l'INSEE. "
                    "L'objectif est de fournir une analyse claire et interactive des inégalités de revenus et des disparités géographiques."
                ),
                html.H4("Données utilisées", className="mt-4"),
                html.P(
                    "Les données proviennent de l'INSEE et incluent :",
                    className="mb-1"
                ),
                html.Ul(
                    [
                        html.Li("Les salaires médians par commune."),
                        html.Li("Les indices de Gini pour mesurer les inégalités de revenus."),
                        html.Li("Les revenus non salariaux et les retraites."),
                    ]
                ),
                html.P(
                    "Nous nous sommes concentrés sur l'Île-de-France car notre jeu de données n'est pas représentatif de l'intégralité des communes françaises. "
                    "Cela nous permet de fournir une analyse plus précise et ciblée."
                ),
                html.H4("Outils et technologies", className="mt-4"),
                html.P(
                    "Ce projet a été réalisé en utilisant les outils suivants :",
                    className="mb-1"
                ),
                html.Ul(
                    [
                        html.Li("Python pour le traitement des données."),
                        html.Li("Dash et Plotly pour la création de tableaux de bord interactifs."),
                        html.Li("GeoJSON pour la visualisation cartographique."),
                        html.Li("Pandas pour la manipulation des données."),
                    ]
                ),
                html.H4("Limites", className="mt-4"),
                html.P(
                    "Ce projet présente certaines limites :",
                    className="mb-1"
                ),
                html.Ul(
                    [
                        html.Li("Les données sont limitées à l'Île-de-France et ne couvrent pas l'ensemble du territoire français."),
                        html.Li("Les données datent de 2018 et ne reflètent pas les évolutions récentes."),
                        html.Li("Certaines communes peuvent avoir des données manquantes ou incomplètes."),
                    ]
                ),
                html.P(
                    "Malgré ces limites, ce projet offre une vision utile des disparités de revenus en Île-de-France."
                ),
            ]
        ),
        className="mb-4 shadow-sm",
    )