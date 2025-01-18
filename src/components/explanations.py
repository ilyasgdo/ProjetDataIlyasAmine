from dash import html
import dash_bootstrap_components as dbc
from typing import Any  

def create_explanations_component() -> Any:
    """
    Crée une partie de texte qui explique ce qu'est l'INSEE, l'indice de Gini et le salaire médian.

    Returns:
        dbc.Card: Un composant Dash Bootstrap contenant les explications.
    """
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4("À propos de l'INSEE, de l'indice de Gini et du salaire médian", className="card-title"),
                html.P(
                    "L'INSEE (Institut National de la Statistique et des Études Économiques) est l'institut national de statistique français. "
                    "Il collecte, produit, analyse et diffuse des informations sur l'économie et la société française."
                ),
                html.P(
                    "L'indice de Gini est une mesure statistique de la dispersion d'une distribution. "
                    "Il est souvent utilisé pour mesurer l'inégalité des revenus au sein d'une population. "
                    "Un indice de Gini de 0 représente une égalité parfaite, tandis qu'un indice de 1 représente une inégalité totale."
                ),
                html.P(
                    "Le salaire médian est la valeur qui sépare la population en deux parts égales : "
                    "50 % des personnes gagnent moins que ce montant et 50 % gagnent plus. "
                    "Contrairement au salaire moyen, le salaire médian est moins sensible aux valeurs extrêmes (très hauts ou très bas salaires), "
                    "ce qui en fait un indicateur plus représentatif de la situation économique de la majorité de la population."
                ),
            ]
        ),
        className="mb-4",
    )