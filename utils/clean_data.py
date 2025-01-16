import os
import pandas as pd


# Chemins des fichiers bruts
RAW_DATA_PATH_ELECTION = os.path.join("data/raw", "rawdataelection.xlsx")
RAW_DATA_PATH_SALAIRE = os.path.join("data/raw", "rawdatasalaire.xlsx")
RAW_DATA_PATH_COMMUNES_ILE_DE_FRANCE = os.path.join(
    "data/raw", "rawdatacommunesiledefrance.csv"
)

# Chemins des fichiers nettoyés
CLEANED_DATA_PATH_SALAIRE = os.path.join("data/cleaned", "cleanedsalaire.xlsx")
CLEANED_DATA_PATH_COMMUNES_ILE_DE_FRANCE = os.path.join(
    "data/cleaned", "cleanedcommunesiledefrance.xlsx"
)


def check_file_exists(file_path: str) -> bool:
    """
    Vérifie si un fichier existe

    Args:
        file_path (str): Le chemin du fichier à vérifier

    Returns:
        bool: True si le fichier existe, sinon False
    """
    return os.path.exists(file_path)


def load_data(file_path: str, skip_rows: int = 0, xlsx: bool = False) -> pd.DataFrame:
    """
    Charge les données depuis un fichier CSV ou Excel, en spécifiant le bon séparateur
    Cette version gère aussi les lignes malformées

    Args:
        file_path (str): Le chemin du fichier à charger
        skip_rows (int): Nombre de lignes à sauter au début du fichier
        xlsx (bool): Si True, charge un fichier Excel, sinon charge un CSV

    Returns:
        pd.DataFrame: Le DataFrame contenant les données du fichier
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier {file_path} n'existe ps")

    try:
        if xlsx:
            # Charger un fichier Excel
            df = pd.read_excel(file_path, skiprows=skip_rows, engine="openpyxl")
        else:
            # Charger un fichier CSV avec un séparateur point-virgule
            df = pd.read_csv(
                file_path,
                skiprows=skip_rows,
                sep=";",
                quotechar='"',
                on_bad_lines="skip",
            )
            # Vérifier et nettoyer les colonnes spécifiques (nomcom ici)
            if "nomcom" in df.columns:
                df = df[
                    "nomcom"
                ].dropna()  # Si des NaN existent, les supprimer de la colonne 'nomcom'

    except Exception as e:
        raise ValueError(f"Erreur lors du chargement du fichier {file_path}: {e}")

    if df.empty:
        raise ValueError("Le fichier est vide ou mal formaté.")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données en supprimant les valeurs manquantes

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données à nettoyer

    Returns:
        pd.DataFrame: Le DataFrame nettoyé
    """
    # Supprimer les lignes avec des NaN
    return df.dropna()


def save_data(df: pd.DataFrame, file_path: str) -> None:
    """
    Sauvegarde les données dans un fichier Excel

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données à sauvegarder
        file_path (str): Le chemin où sauvegarder les données
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_excel(file_path, index=False)


def clean_data_process(
    raw_path: str, cleaned_path: str, skip_rows: int, xlsx: bool = True
) -> None:
    """
    Fonction principale pour le nettoyage des données :
    charge les données, les nettoie, et les sauvegarde

    Args:
        raw_path (str): Chemin des données brutes
        cleaned_path (str): Chemin des données nettoyées
        skip_rows (int): Nombre de lignes à sauter au début des données brutes
    """
    try:
        df = load_data(raw_path, skip_rows=skip_rows, xlsx=xlsx)
        df_cleaned = clean_data(df)
        save_data(df_cleaned, cleaned_path)
        print(f"Données nettoyées et sauvegardées dans : {cleaned_path}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Erreur lors du nettoyage des données : {e}")
        exit(1)


def clean_all_raw_files() -> None:
    """
    Nettoie tous les fichiers de données brutes et sauvegarde les résultats nettoyés
    """

    if not os.path.isfile(CLEANED_DATA_PATH_SALAIRE):
        clean_data_process(RAW_DATA_PATH_SALAIRE, CLEANED_DATA_PATH_SALAIRE, 5)

    if not os.path.isfile(CLEANED_DATA_PATH_COMMUNES_ILE_DE_FRANCE):
        clean_data_process(
            RAW_DATA_PATH_COMMUNES_ILE_DE_FRANCE,
            CLEANED_DATA_PATH_COMMUNES_ILE_DE_FRANCE,
            0,
            xlsx=False,
        )


if __name__ == "__main__":
    clean_all_raw_files()
