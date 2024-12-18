from dash import html

def create_header():
    """Retourne un header simple pour l'application."""
    return html.Header(children=[
        html.H1("Bienvenue sur la Visualisation des Salaires Médians et Indice de Gini", style={'textAlign': 'center', 'color': '#333'})
    ])
