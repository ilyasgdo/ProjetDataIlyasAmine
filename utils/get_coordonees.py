import os
import requests
import pandas as pd
import urllib.parse
from typing import Optional, Tuple, List

# Chemins des fichiers
CHEMIN_DONNEES_ENTREE = os.path.join("data", "cleaned", "cleanedcommunesiledefrance.xlsx")
CHEMIN_DONNEES_SORTIE = os.path.join("data", "cleaned", "cleanedcoordonnees.xlsx")

def charger_donnees(file_path: str) -> pd.DataFrame:
    """
    Charge les données depuis un fichier Excel.

    Args:
        file_path (str): Le chemin du fichier Excel.

    Returns:
        pd.DataFrame: Le DataFrame contenant les données chargées.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
    
    return pd.read_excel(file_path)

def recuperer_coordonnees(ville: str) -> Tuple[str, Optional[float], Optional[float]]:
    """
    Récupère les coordonnées géographiques d'une ville via l'API Adresse.

    Args:
        ville (str): Le nom de la ville.

    Returns:
        Tuple[str, Optional[float], Optional[float]]: Nom de la ville, latitude, longitude.
    """
    api_url = "https://api-adresse.data.gouv.fr/search/?q="
    try:
        response = requests.get(api_url + urllib.parse.quote(ville))
        response.raise_for_status()
        data = response.json()
        if data["features"]:
            longitude, latitude = data["features"][0]["geometry"]["coordinates"]
            return ville, latitude, longitude
        return ville, None, None
    except requests.RequestException:
        return ville, None, None

def sauvegarder_donnees(df: pd.DataFrame, file_path: str) -> None:
    """
    Sauvegarde un DataFrame dans un fichier Excel.

    Args:
        df (pd.DataFrame): Le DataFrame à sauvegarder.
        file_path (str): Le chemin du fichier Excel où sauvegarder les données.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_excel(file_path, index=False)

def extraire_coordonnees(file_path_entree: str, file_path_sortie: str) -> None:
    """
    Charge un fichier contenant des noms de villes, récupère leurs coordonnées
    géographiques et sauvegarde les résultats.

    Args:
        file_path_entree (str): Chemin du fichier d'entrée contenant les noms de villes.
        file_path_sortie (str): Chemin du fichier de sortie pour enregistrer les coordonnées.
    """
    try:
        # Charger les données
        data = charger_donnees(file_path_entree)
        
        # Extraire les noms uniques des villes
        villes_uniques: List[str] = data["nomcom"].drop_duplicates().dropna().tolist()

        # Récupérer les coordonnées pour chaque ville
        resultats = [recuperer_coordonnees(ville) for ville in villes_uniques]

        # Transformer les résultats en DataFrame
        df_resultats = pd.DataFrame(resultats, columns=["Ville", "Latitude", "Longitude"])

        # Sauvegarder les résultats
        sauvegarder_donnees(df_resultats, file_path_sortie)
        print(f"Les coordonnées ont été sauvegardées dans {file_path_sortie}")

    except (FileNotFoundError, KeyError) as e:
        print(f"Erreur lors du traitement des données : {e}")
        exit(1)

if __name__ == "__main__":
    extraire_coordonnees(CHEMIN_DONNEES_ENTREE, CHEMIN_DONNEES_SORTIE)
