from dash import html
import dash_bootstrap_components as dbc

def create_header() -> html.Header:
    """
    Crée un en-tête stylisé pour l'application avec Dash Bootstrap Components

    Returns:
        html.Header: Un en-tête HTML stylisé contenant le titre de l'application
    """
    return html.Header(
        dbc.Container(
            fluid=True,
            children=[
                dbc.Row(
                    dbc.Col(
                        html.H1(
                            "Visualisation des Divers revenues en  Île-de-France",
                            className="text-center my-4 text-primary",
                        ),
                        width={"size": 8, "offset": 2},  
                    ),
                ),
                dbc.Row(
                    dbc.Col(
                        html.P(
                            "Une application pour explorer les inégalités et les salaires médians par commune.",
                            className="text-center text-muted mb-0",
                        ),
                        width={"size": 8, "offset": 2},
                    ),
                ),
            ],
            className="bg-light p-4 shadow-sm", 
        )
    )
