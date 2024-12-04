import pandas as pd
import os
import openpyxl


destination_directory = "data/raw"
RAW_DATA_PATH = os.path.join(destination_directory, "rawdata.xlsx")

destination_directory = "data/cleaned"
CLEANED_DATA_PATH  = os.path.join(destination_directory, "cleaned.xlsx")

if not os.path.exists(RAW_DATA_PATH):
    print(f"Le fichier {RAW_DATA_PATH} n'existe pas.")
    exit()

def clean_data():
    df = pd.read_excel(RAW_DATA_PATH)
    df = df.dropna()  
    df.to_excel(CLEANED_DATA_PATH, index=False)
    print("Data cleaned and saved.")

if __name__ == "__main__":
    clean_data()
