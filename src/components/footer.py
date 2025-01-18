from dash import html
import dash_bootstrap_components as dbc

def create_footer() -> html.Footer:
    """
    Crée un pied de page avec Dash Bootstrap Components

    Returns:
        html.Footer: Un footer HTML 
    """
    return html.Footer(
        dbc.Container(
            fluid=True,
            children=[
                dbc.Row(
                    dbc.Col(
                        html.P(
                            "© 2025 Ilyas Amine ",
                            className="text-center text-muted my-3",
                        ),
                        width=12,  
                    ),
                ),
            ],
            className="bg-dark text-light py-3 shadow-lg", 
        )
    )
