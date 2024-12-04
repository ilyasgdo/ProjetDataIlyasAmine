import pandas as pd
import os

RAW_DATA_PATH = os.path.join("data/raw", "rawdata.xlsx")
CLEANED_DATA_PATH = os.path.join("data/cleaned", "cleaned.xlsx")

def check_file_exists(file_path: str) -> bool:
    """
    Vérifie si un fichier existe.

    Args:
        file_path (str): Le chemin du fichier à vérifier.

    Returns:
        bool: True si le fichier existe, sinon False.
    """
    return os.path.exists(file_path)

def load_data(file_path: str) -> pd.DataFrame:
    """
    Charge les données depuis un fichier Excel.

    Args:
        file_path (str): Le chemin du fichier Excel à charger.

    Returns:
        pd.DataFrame: Le DataFrame contenant les données du fichier.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
        ValueError: Si le fichier est vide ou mal formaté.
    """
    if not check_file_exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
    
    df = pd.read_excel(file_path)

    if df.empty:
        raise ValueError("Le fichier est vide ou mal formaté.")
    
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données en supprimant les valeurs manquantes.

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données à nettoyer.

    Returns:
        pd.DataFrame: Le DataFrame nettoyé, sans valeurs manquantes.
    """
    return df.dropna()

def save_data(df: pd.DataFrame, file_path: str):
    """
    Sauvegarde les données dans un fichier Excel.

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données à sauvegarder.
        file_path (str): Le chemin où sauvegarder les données.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_excel(file_path, index=False)

def clean_data_process():
    """
    Fonction principale pour le nettoyage des données : 
    charge les données, les nettoie, et les sauvegarde.
    """
    try:
        df = load_data(RAW_DATA_PATH)
        df_cleaned = clean_data(df)
        save_data(df_cleaned, CLEANED_DATA_PATH)
        print("Données nettoyées et sauvegardées.")
    except (FileNotFoundError, ValueError) as e:
        print(str(e))
        exit(1)

if __name__ == "__main__":
    clean_data_process()
