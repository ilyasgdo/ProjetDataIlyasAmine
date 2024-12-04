import os
import requests

# URL 
url = "https://static.data.gouv.fr/resources/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/20220414-152612/resultats-par-niveau-burvot-t1-france-entiere.xlsx"

# Chemin vers le dossier
destination_directory = "data/raw"
destination_file = os.path.join(destination_directory, "rawdata.xlsx")

os.makedirs(destination_directory, exist_ok=True)

try:
    # Télécharger le fichier
    response = requests.get(url, stream=True)
    response.raise_for_status()  

    
    with open(destination_file, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Fichier téléchargé avec succès dans : {destination_file}")

except requests.exceptions.RequestException as e:
    print(f"Erreur lors du téléchargement : {e}")
