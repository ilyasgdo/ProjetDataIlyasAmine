from data.get_data import get_data
from dashboard.app import app
from dashboard.layout import layout
from dashboard.callbacks import register_callbacks

def main() -> None:
    data = get_data()  # Supposons que get_data retourne un DataFrame
    print(data.head())

if __name__ == "__main__":
    main()
