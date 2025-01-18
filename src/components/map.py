import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from typing import Optional, Dict, Any

GEOJSON_PATH: str = "data/geojson/communesiledefrance.geojson"

def load_geojson(file_path: str) -> Dict[str, Any]:
    """
    Charge un fichier GeoJSON à partir du chemin donné

    Args:
        file_path (str): Chemin du fichier GeoJSON

    Returns:
        dict: Données GeoJSON chargées
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def create_dataframe_from_geojson(geojson_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Extrait les propriétés des communes depuis les données GeoJSON 
    et les transforme en DataFrame

    Args:
        geojson_data (dict): Données GeoJSON

    Returns:
        pd.DataFrame: DataFrame contenant les informations des communes
    """
    return pd.DataFrame([
        {
            "nom": feature["properties"].get("nom", "Inconnu"),
            "Mediane": feature["properties"].get("mediane_salaire_moyenne", None),
            "Indice": feature["properties"].get("indice_gini_moyen", None),
            "codeDepartement": feature["properties"].get("codeDepartement", "Inconnu")
        }
        for feature in geojson_data.get("features", [])
    ])

def create_map_component(app: Dash, geojson_data: Dict[str, Any], df_data: pd.DataFrame) -> html.Div:
    """
    Crée une section de mise en page contenant la carte dynamique

    Args:
        app (Dash): l'application Dash
        geojson_data (dict): Données GeoJSON utilisées pour la carte
        df_data (pd.DataFrame): Données des communes

    Returns:
        html.Div: Mise en page HTML contenant la carte dynamique
    """
    layout = html.Div(
        children=[
            html.Div(
                [
                    html.Label("Choisissez une métrique :", style={"fontWeight": "bold"}),
                    dcc.RadioItems(
                        id="metric-selector",
                        options=[
                            {"label": "Salaires médians", "value": "Mediane"},
                            {"label": "Indices de Gini", "value": "Indice"}
                        ],
                        value="Mediane",
                        inline=False,
                        style={"marginBottom": "10px"}
                    ),
                ],
                style={"marginBottom": "20px"}
            ),
            html.Div(
                [
                    html.Label("Filtrer par département :", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        id="departement-filter",
                        options=[
                            {"label": dept, "value": dept} for dept in df_data["codeDepartement"].unique()
                        ],
                        multi=True,
                        placeholder="Sélectionnez un ou plusieurs départements",
                        style={"marginBottom": "20px"}
                    ),
                ],
                style={"marginBottom": "20px"}
            ),
            html.Div(
                id="map-description",
                children=[
                    html.H3(id="map-title", className="text-center"),
                    html.P(id="map-text", className="text-center")
                ],
                style={"marginBottom": "20px"}
            ),
            dcc.Graph(id="map-graph", style={"height": "75vh"}),
        ],
        style={"padding": "20px", "backgroundColor": "#ffffff", "borderRadius": "10px"}
    )

    @app.callback(
        [Output("map-graph", "figure"), Output("map-title", "children"), Output("map-text", "children")],
        [Input("metric-selector", "value"), Input("departement-filter", "value")]
    )
    def update_map(selected_metric: str, departements: Optional[list[str]]) -> tuple[px.choropleth_mapbox, str, str]:
        """
        Met à jour la carte interactive, le titre et le texte explicatif en fonction de la métrique et des départements sélectionnés

        Args:
            selected_metric (str): Métrique sélectionnée ("Mediane" ou "Indice")
            departements (Optional[list[str]]): Liste des départements sélectionnés

        Returns:
            tuple: La carte interactive mise à jour, le titre et le texte explicatif
        """
        # filtrer les data
        filtered_data = df_data[df_data["codeDepartement"].isin(departements)] if departements else df_data

        # créer la carte
        fig = px.choropleth_mapbox(
            filtered_data,
            geojson=geojson_data,
            color=selected_metric,
            locations="nom",
            featureidkey="properties.nom",
            mapbox_style="open-street-map",
            center={"lat": 48.8566, "lon": 2.3522},
            zoom=9,
            hover_name="nom"
        )

        # configurer les détails de la carte
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_colorbar={"title": "Valeur"}
        )

        # définir le titre et le texte explicatif en fonction de la métrique (gini ou median)
        if selected_metric == "Mediane":
            title = "Carte des salaires médians en Île-de-France"
            text = (
                "Le salaire médian est la valeur qui sépare la population en deux parts égales : "
                "50 % des personnes gagnent moins que ce montant et 50 % gagnent plus. "
                "Il est un indicateur clé pour comprendre les inégalités de revenus."
            )
        else:
            title = "Carte des indices de Gini en Île-de-France"
            text = (
                "L'indice de Gini mesure les inégalités de revenus au sein d'une population. "
                "Un indice de 0 représente une égalité parfaite, tandis qu'un indice de 1 représente une inégalité totale."
            )

        return fig, title, text

    return layout