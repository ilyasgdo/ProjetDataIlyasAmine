import os
import requests
from typing import Any

# URLs des fichiers à télécharger
URL_ELECTION = "https://static.data.gouv.fr/resources/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/20220414-152612/resultats-par-niveau-burvot-t1-france-entiere.xlsx"
URL_SALAIRE = "https://www.insee.fr/fr/statistiques/fichier/5055909/BASE_TD_FILO_DEC_IRIS_2018.xlsx"
URL_COMMUNES_ILE_DE_FRANCE = (
    "https://www.data.gouv.fr/fr/datasets/r/91c0bdc4-0a5b-4ac8-950e-64a1ec207957"
)

# Répertoires et fichiers de destination
DESTINATION_DIRECTORY = "data/raw"
DESTINATION_FILE_ELECTION = os.path.join(DESTINATION_DIRECTORY, "rawdataelection.xlsx")
DESTINATION_FILE_SALAIRE = os.path.join(DESTINATION_DIRECTORY, "rawdatasalaire.xlsx")
DESTINATION_FILE_COMMUNES_ILE_DE_FRANCE = os.path.join(
    DESTINATION_DIRECTORY, "rawdatacommunesiledefrance.csv"
)

# Création du répertoire de destination si nécessaire
os.makedirs(DESTINATION_DIRECTORY, exist_ok=True)


def download_data(url: str, destination_file: str) -> None:
    """
    Télécharge les données depuis une URL vers un fichier local.

    Args:
        url (str): URL du fichier à télécharger.
        destination_file (str): Chemin complet du fichier de destination.

    Raises:
        SystemExit: Si une erreur survient lors du téléchargement.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(destination_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Vérifie que le chunk n'est pas vide
                    file.write(chunk)

        print(f"Fichier téléchargé avec succès dans : {destination_file}")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")
        exit(1)


def download_all_data() -> None:
    """
    Télécharge tous les fichiers de données si ils n'existent pas déjà localement.
    """
    if not os.path.isfile(DESTINATION_FILE_ELECTION):
        download_data(URL_ELECTION, DESTINATION_FILE_ELECTION)

    if not os.path.isfile(DESTINATION_FILE_SALAIRE):
        download_data(URL_SALAIRE, DESTINATION_FILE_SALAIRE)

    if not os.path.isfile(DESTINATION_FILE_COMMUNES_ILE_DE_FRANCE):
        download_data(
            URL_COMMUNES_ILE_DE_FRANCE, DESTINATION_FILE_COMMUNES_ILE_DE_FRANCE
        )


if __name__ == "__main__":
    download_all_data()
