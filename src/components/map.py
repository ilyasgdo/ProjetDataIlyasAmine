import json
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from typing import Optional

# Définir les chemins des fichiers
GEOJSON_PATH: str = "data/geojson/communesiledefrance.geojson"

def load_geojson(file_path: str) -> dict:
    """
    Charge un fichier GeoJSON à partir du chemin donné.

    Args:
        file_path (str): Chemin du fichier GeoJSON.

    Returns:
        dict: Données GeoJSON chargées.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def create_dataframe_from_geojson(geojson_data: dict) -> pd.DataFrame:
    """
    Extrait les propriétés des communes depuis les données GeoJSON 
    et les transforme en DataFrame.

    Args:
        geojson_data (dict): Données GeoJSON.

    Returns:
        pd.DataFrame: DataFrame contenant les informations des communes.
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

def create_map_component(app: Dash, geojson_data: dict, df_data: pd.DataFrame) -> html.Div:
    """
    Crée une section de mise en page contenant la carte interactive.

    Args:
        app (Dash): Instance de l'application Dash.
        geojson_data (dict): Données GeoJSON utilisées pour la carte.
        df_data (pd.DataFrame): Données des communes.

    Returns:
        html.Div: Mise en page HTML contenant la carte interactive.
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
            dcc.Graph(id="map-graph", style={"height": "75vh"}),
        ],
        style={"padding": "20px", "backgroundColor": "#ffffff", "borderRadius": "10px"}
    )

    @app.callback(
        Output("map-graph", "figure"),
        [Input("metric-selector", "value"), Input("departement-filter", "value")]
    )
    def update_map(selected_metric: str, departements: Optional[list[str]]) -> px.choropleth_mapbox:
        """
        Met à jour la carte interactive en fonction de la métrique et des départements sélectionnés.

        Args:
            selected_metric (str): Métrique sélectionnée ("Mediane" ou "Indice").
            departements (Optional[list[str]]): Liste des départements sélectionnés.

        Returns:
            px.choropleth_mapbox: Carte interactive mise à jour.
        """
        # Filtrer les données
        filtered_data = df_data[df_data["codeDepartement"].isin(departements)] if departements else df_data

        # Créer la carte
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

        # Configurer les détails de la carte
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_colorbar={"title": "Valeur"}
        )
        return fig

    return layout

def main() -> None:
    """
    Point d'entrée principal de l'application Dash.
    """
    app = Dash(__name__)

    geojson_data = load_geojson(GEOJSON_PATH)
    df_data = create_dataframe_from_geojson(geojson_data)
    app.layout = create_map_component(app, geojson_data, df_data)

    app.run_server(debug=True)

if __name__ == "__main__":
    main()
