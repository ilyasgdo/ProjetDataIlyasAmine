from dash import html


def create_footer():
    """Retourne un footer simple pour l'application."""
    return html.Footer(
        children=[
            html.P(
                "© 2024 Votre Nom - Tous droits réservés",
                style={"textAlign": "center", "color": "#777"},
            ),
        ]
    )
