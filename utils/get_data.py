import os
import requests

# URL 
url = "https://static.data.gouv.fr/resources/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/20220414-152612/resultats-par-niveau-burvot-t1-france-entiere.xlsx"

destination_directory = "data/raw"
destination_file = os.path.join(destination_directory, "rawdata.xlsx")


os.makedirs(destination_directory, exist_ok=True)

def download_data(url: str, destination_file: str):
    """Télécharge les données à partir de l'URL vers un fichier local."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  

        with open(destination_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Fichier téléchargé avec succès dans : {destination_file}")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")
        exit(1)  

if __name__ == "__main__":
    download_data(url, destination_file)
