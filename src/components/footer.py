from dash import html
import dash_bootstrap_components as dbc

def create_footer() -> html.Footer:
    """
    Crée un pied de page stylisé pour l'application avec Dash Bootstrap Components.

    Returns:
        html.Footer: Un pied de page HTML contenant des informations de copyright.
    """
    return html.Footer(
        dbc.Container(
            fluid=True,
            children=[
                dbc.Row(
                    dbc.Col(
                        html.P(
                            "© 2024 Ilyas Amine - Tous droits réservés",
                            className="text-center text-muted my-3",
                        ),
                        width=12,  # S'étend sur toute la largeur
                    ),
                ),
            ],
            className="bg-dark text-light py-3 shadow-lg",  # Fond sombre avec du texte clair et une ombre
        )
    )
