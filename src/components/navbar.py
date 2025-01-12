import dash_bootstrap_components as dbc


def create_navbar() -> dbc.Navbar:
    """
    Crée une barre de navigation stylisée avec Bootstrap pour l'application.

    Returns:
        dbc.Navbar: Une barre de navigation réactive et élégante.
    """
    # Élément de navigation
    navbar = dbc.Navbar(
        color="primary",
        dark=True,
        children=[
            dbc.Container(
                [
                    dbc.NavbarBrand(
                        "Visualisation IDF",
                        href="/",
                        className="ms-3",
                        style={"fontWeight": "bold", "fontSize": "1.5rem"},
                    ),
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                dbc.NavLink("Accueil", href="/", active=True)
                            ),
                            dbc.NavItem(
                                dbc.NavLink("Graphiques", href="#graph")
                            ),
                            dbc.NavItem(
                                dbc.NavLink("À propos", href="#about")
                            ),
                        ],
                        className="ms-auto",
                    ),
                ],
                fluid=True,
            )
        ],
    )
    return navbar
