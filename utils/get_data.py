import os
import requests

# URL 
url_election = "https://static.data.gouv.fr/resources/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/20220414-152612/resultats-par-niveau-burvot-t1-france-entiere.xlsx"
url_salaire = "https://www.insee.fr/fr/statistiques/fichier/5055909/BASE_TD_FILO_DEC_IRIS_2018.xlsx"

destination_directory = "data/raw"
destination_file_election = os.path.join(destination_directory, "rawdataelection.xlsx")
destination_file_salaire = os.path.join(destination_directory, "rawdatasalaire.xlsx")

os.makedirs(destination_directory, exist_ok=True)

def download_data(url: str, destination_file: str) -> None :
    """Télécharge les données à partir de l'URL vers un fichier local."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  

        with open(destination_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                print(chunk)

        print(f"Fichier téléchargé avec succès dans : {destination_file}")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")
        exit(1)  

if __name__ == "__main__":
    download_data(url_election, destination_file_election)
    download_data(url_salaire, destination_file_salaire)
