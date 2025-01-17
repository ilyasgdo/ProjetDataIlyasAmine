import json
import requests
import pandas as pd
import geopandas as gpd
from typing import List, Dict, Any

# Constantes
API_URL = "https://geo.api.gouv.fr/communes?nom={}&fields=contour,codeRegion,codesPostaux&format=geojson&geometry=contour"
CODE_REGION_IDF = "11"
ARRONDISSEMENTS_GEOJSON_PATH = "data/geojson/arrondissements.geojson"
OUTPUT_GEOJSON_PATH = "data/geojson/communesiledefrance.geojson"
EXCEL_COORDONNEES = "data/cleaned/cleanedcoordonnees.xlsx"
EXCEL_SALAIRES = "data/cleaned/cleanedsalaire.xlsx"

def charger_villes_depuis_excel(fichier_excel: str) -> List[str]:
    """
    Charge les noms des villes depuis un fichier Excel.

    Args:
        fichier_excel (str): Chemin du fichier Excel.

    Returns:
        List[str]: Liste des noms de villes.
    """
    villes_df = pd.read_excel(fichier_excel).iloc[1:]  # Suppression de l'entête inutile
    return villes_df.iloc[:, 0].dropna().unique().tolist()


def nettoyer_donnees_salaires(fichier_salaire: str) -> pd.DataFrame:
    """
    Nettoie et prépare les données de salaires.

    Args:
        fichier_salaire (str): Chemin du fichier Excel des salaires.

    Returns:
        pd.DataFrame: Données de salaires nettoyées et agrégées.
    """
    salaire_data = pd.read_excel(fichier_salaire)
    salaire_data_cleaned = salaire_data.rename(columns={salaire_data.columns[2]: "code_commune"})
    salaire_data_cleaned["code_commune"] = salaire_data_cleaned["code_commune"].astype(str).str.zfill(5)
    salaire_data_cleaned.iloc[:, 7] = pd.to_numeric(salaire_data_cleaned.iloc[:, 7], errors="coerce")
    salaire_data_cleaned.iloc[:, 20] = pd.to_numeric(salaire_data_cleaned.iloc[:, 20], errors="coerce")

    salaire_data_grouped = salaire_data_cleaned.groupby("code_commune").agg({
        salaire_data_cleaned.columns[7]: "mean",
        salaire_data_cleaned.columns[20]: "mean"
    }).reset_index()

    salaire_data_grouped.rename(columns={
        salaire_data_cleaned.columns[7]: "mediane_salaire_moyenne",
        salaire_data_cleaned.columns[20]: "indice_gini_moyen"
    }, inplace=True)

    return salaire_data_grouped


def recuperer_contours_villes(villes: List[str]) -> List[Dict[str, Any]]:
    """
    Récupère les contours des villes depuis l'API geo.api.gouv.fr.

    Args:
        villes (List[str]): Liste des noms de villes.

    Returns:
        List[Dict[str, Any]]: Liste des features GeoJSON pour les villes.
    """
    features = []
    for ville in villes:
        try:
            response = requests.get(API_URL.format(ville))
            data = response.json()

            if "features" in data:
                for feature in data["features"]:
                    if feature["properties"]["codeRegion"] == CODE_REGION_IDF:
                        codes_postaux = feature["properties"].get("codesPostaux", [])
                        code_departement = codes_postaux[0][:2] if codes_postaux else "Inconnu"
                        feature["properties"]["codeDepartement"] = code_departement
                        features.append(feature)
        except Exception as e:
            print(f"Erreur pour la ville {ville}: {e}")
    return features


def charger_contours_arrondissements(fichier_geojson: str) -> List[Dict[str, Any]]:
    """
    Charge les contours des arrondissements de Paris depuis un fichier GeoJSON.

    Args:
        fichier_geojson (str): Chemin du fichier GeoJSON.

    Returns:
        List[Dict[str, Any]]: Liste des features GeoJSON des arrondissements.
    """
    try:
        arrondissements_gdf = gpd.read_file(fichier_geojson)
        arrondissement_codes = {
            "1er Ardt": "75101", "2ème Ardt": "75102", "3ème Ardt": "75103", "4ème Ardt": "75104",
            "5ème Ardt": "75105", "6ème Ardt": "75106", "7ème Ardt": "75107", "8ème Ardt": "75108",
            "9ème Ardt": "75109", "10ème Ardt": "75110", "11ème Ardt": "75111", "12ème Ardt": "75112",
            "13ème Ardt": "75113", "14ème Ardt": "75114", "15ème Ardt": "75115", "16ème Ardt": "75116",
            "17ème Ardt": "75117", "18ème Ardt": "75118", "19ème Ardt": "75119", "20ème Ardt": "75120"
        }

        features = []
        for _, row in arrondissements_gdf.iterrows():
            arrondissement_nom = row["l_ar"]
            code_insee = arrondissement_codes.get(arrondissement_nom, "Inconnu")
            features.append({
                "type": "Feature",
                "geometry": row["geometry"].__geo_interface__,
                "properties": {
                    "nom": row["l_ar"],
                    "code": code_insee,
                    "codeRegion": "11",
                    "codeDepartement": "75",
                    "surface": row.get("surface", None),
                    "perimetre": row.get("perimetre", None)
                }
            })
        return features
    except Exception as e:
        print(f"Erreur lors de l'ajout des arrondissements de Paris : {e}")
        return []


def generer_geojson_final(villes_features: List[Dict[str, Any]], arrondissements_features: List[Dict[str, Any]],
                          salaire_data: pd.DataFrame, output_path: str) -> None:
    """
    Génère un fichier GeoJSON final combinant les données des villes, arrondissements et salaires.

    Args:
        villes_features (List[Dict[str, Any]]): Features GeoJSON des villes.
        arrondissements_features (List[Dict[str, Any]]): Features GeoJSON des arrondissements.
        salaire_data (pd.DataFrame): Données de salaires.
        output_path (str): Chemin de sortie pour le fichier GeoJSON.

    Returns:
        None
    """
    features = villes_features + arrondissements_features
    for feature in features:
        code_commune = feature["properties"].get("code")
        if code_commune and code_commune in salaire_data["code_commune"].values:
            salaire_info = salaire_data[salaire_data["code_commune"] == code_commune].iloc[0]
            feature["properties"]["mediane_salaire_moyenne"] = salaire_info["mediane_salaire_moyenne"]
            feature["properties"]["indice_gini_moyen"] = salaire_info["indice_gini_moyen"]
        else:
            feature["properties"]["mediane_salaire_moyenne"] = None
            feature["properties"]["indice_gini_moyen"] = None

    geojson_final = {"type": "FeatureCollection", "features": features}
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(geojson_final, file, ensure_ascii=False, indent=2)
    print(f"Fichier GeoJSON complet généré : {output_path}")


if __name__ == "__main__":
    villes = charger_villes_depuis_excel(EXCEL_COORDONNEES)
    salaire_data = nettoyer_donnees_salaires(EXCEL_SALAIRES)
    villes_features = recuperer_contours_villes(villes)
    arrondissements_features = charger_contours_arrondissements(ARRONDISSEMENTS_GEOJSON_PATH)
    generer_geojson_final(villes_features, arrondissements_features, salaire_data, OUTPUT_GEOJSON_PATH)
