from dash import html, dcc

def create_navbar():
    """Retourne une barre de navigation simple."""
    return html.Nav(children=[
        html.Ul(children=[
            html.Li(dcc.Link("Accueil", href="/", style={'padding': '10px', 'textDecoration': 'none'})),
            html.Li(dcc.Link("Graphiques", href="#graph", style={'padding': '10px', 'textDecoration': 'none'})),
            html.Li(dcc.Link("À propos", href="#about", style={'padding': '10px', 'textDecoration': 'none'})),
        ], style={'listStyleType': 'none', 'display': 'flex', 'justifyContent': 'center', 'backgroundColor': '#f8f9fa'})
    ])
