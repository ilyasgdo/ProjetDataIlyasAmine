import pandas as pd
import os

RAW_DATA_PATH_ELECTION = os.path.join("data/raw", "rawdataelection.xlsx")
RAW_DATA_PATH_SALAIRE = os.path.join("data/raw", "rawdatasalaire.xlsx")

CLEANED_DATA_PATH_ELECTION = os.path.join("data/cleaned", "cleanedelection.xlsx")
CLEANED_DATA_PATH_SALAIRE = os.path.join("data/cleaned", "cleanedsalaire.xlsx")

def check_file_exists(file_path: str) -> bool:
    """
    Vérifie si un fichier existe.

    Args:
        file_path (str): Le chemin du fichier à vérifier.

    Returns:
        bool: True si le fichier existe, sinon False.
    """
    return os.path.exists(file_path)

def load_data(file_path: str, skip_rows: int = 0) -> pd.DataFrame:
    """
    Charge les données depuis un fichier Excel, avec une option pour sauter des lignes.

    Args:
        file_path (str): Le chemin du fichier Excel à charger.
        skip_rows (int): Nombre de lignes à sauter au début du fichier.

    Returns:
        pd.DataFrame: Le DataFrame contenant les données du fichier.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
        ValueError: Si le fichier est vide ou mal formaté.
    """
    if not check_file_exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
    
    df = pd.read_excel(file_path, skiprows=skip_rows)  # Sauter les lignes inutiles
    
    if df.empty:
        raise ValueError("Le fichier est vide ou mal formaté.")
    
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données en supprimant les valeurs manquantes, et 

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données à nettoyer.

    Returns:
        pd.DataFrame: Le DataFrame nettoyé.
    """
    
    
    return df.dropna()

def save_data(df: pd.DataFrame, file_path: str)-> None:
    """
    Sauvegarde les données dans un fichier Excel.

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données à sauvegarder.
        file_path (str): Le chemin où sauvegarder les données.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_excel(file_path, index=False)

def clean_data_process(raw_path: str, cleaned_path: str, skip_rows: int)-> None:
    """
    Fonction principale pour le nettoyage des données : 
    charge les données, les nettoie, et les sauvegarde.

    Args:
        raw_path (str): Chemin des données brutes.
        cleaned_path (str): Chemin des données nettoyées.
        remove_first_rows (bool): Si True, supprime les 4 premières lignes.
    """
    try:
        df = load_data(raw_path, skip_rows=skip_rows)
        df_cleaned = clean_data(df)
        print(df_cleaned)
        save_data(df_cleaned, cleaned_path)
        print("Données nettoyées et sauvegardées.")
    except (FileNotFoundError, ValueError) as e:
        print(str(e))
        exit(1)

if __name__ == "__main__":
    # Processus de nettoyage pour chaque fichier
    #clean_data_process(RAW_DATA_PATH_ELECTION, CLEANED_DATA_PATH_ELECTION, 0)
    clean_data_process(RAW_DATA_PATH_SALAIRE, CLEANED_DATA_PATH_SALAIRE, 5)
