import os
import requests

URL_SALAIRE = "https://www.insee.fr/fr/statistiques/fichier/5055909/BASE_TD_FILO_DEC_IRIS_2018.xlsx"
URL_COMMUNES_ILE_DE_FRANCE = (
    "https://www.data.gouv.fr/fr/datasets/r/91c0bdc4-0a5b-4ac8-950e-64a1ec207957"
)

# Répertoires et fichiers de destination
DESTINATION_DIRECTORY = "data/raw"
DESTINATION_FILE_SALAIRE = os.path.join(DESTINATION_DIRECTORY, "rawdatasalaire.xlsx")
DESTINATION_FILE_COMMUNES_ILE_DE_FRANCE = os.path.join(
    DESTINATION_DIRECTORY, "rawdatacommunesiledefrance.csv"
)

# Création du répertoire de destination si nécessaire
os.makedirs(DESTINATION_DIRECTORY, exist_ok=True)


def download_data(url: str, destination_file: str) -> bool:
    """
    Télécharge les données depuis une URL vers un fichier local

    Args:
        url (str): URL du fichier à télécharger
        destination_file (str): Chemin complet du fichier de destination

    Returns:
        bool: True si le téléchargement a réussi, False sinon
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(destination_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Vérifie que le chunk n'est pas vide
                    file.write(chunk)

        print(f"Fichier téléchargé avec succès dans : {destination_file}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de {url} : {e}")
        return False


def is_file_valid(file_path: str) -> bool:
    """
    Vérifie si un fichier existe et n'est pas vide

    Args:
        file_path (str): Chemin du fichier à vérifier

    Returns:
        bool: True si le fichier existe et n'est pas vide, False sinon
    """
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0


def download_all_data() -> None:
    """
    Télécharge tous les fichiers de données si ils n'existent pas déjà localement ou s'ils sont vides
    """
    # Télécharger les fichiers uniquement s'ils n'existent pas ou sont vides
    if not is_file_valid(DESTINATION_FILE_SALAIRE):
        print("Téléchargementsalaires...")
        if not download_data(URL_SALAIRE, DESTINATION_FILE_SALAIRE):
            print("Échec du téléchargement salaires")

    if not is_file_valid(DESTINATION_FILE_COMMUNES_ILE_DE_FRANCE):
        print("Téléchargement communes d'Île-de-France...")
        if not download_data(URL_COMMUNES_ILE_DE_FRANCE, DESTINATION_FILE_COMMUNES_ILE_DE_FRANCE):
            print("Échec du téléchargement communes d'Île-de-France")


if __name__ == "__main__":
    download_all_data()