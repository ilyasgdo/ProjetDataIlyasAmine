# src/components/filters.py
from dash import dcc, html
import pandas as pd


def generate_filters(df: pd.DataFrame) -> html.Div:
    regions = df["LIBCOM"].unique()  # Villes uniques
    data_types = [
        {"label": "Salaire Médian", "value": "DEC_MED18"},
        {"label": "Quantile Q1", "value": "DEC_Q118"},
        {"label": "Quantile Q3", "value": "DEC_Q318"},
        {"label": "Indice de Gini", "value": "DEC_GI18"},
        {"label": "Taux de Chômage", "value": "DEC_TP6018"},
    ]

    return html.Div(
        [
            # Sélecteur de région
            html.Div(
                [
                    html.Label("Sélectionnez une ville :"),
                    dcc.Dropdown(
                        id="region-selector",
                        options=[
                            {"label": region, "value": region}
                            for region in sorted(regions)
                        ],
                        value=None,  # Pas de valeur par défaut
                        placeholder="Choisissez une ville",
                    ),
                ],
                style={"margin-bottom": "20px"},
            ),
            # Sélecteur de type de données
            html.Div(
                [
                    html.Label("Sélectionnez un type de donnée :"),
                    dcc.Dropdown(
                        id="data-type-selector",
                        options=data_types,
                        value="DEC_MED18",  # Par défaut, salaire médian
                        placeholder="Choisissez un type de donnée",
                    ),
                ],
                style={"margin-bottom": "20px"},
            ),
        ]
    )
