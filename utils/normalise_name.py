import re
import unicodedata

def normalize_name(name:str) ->str:
    """Nettoyer et normaliser un nom en ne conservant que les lettres, et en les mettant en minuscules."""
    # Supprimer les caractères non alphabétiques et normaliser les accents
    name = ''.join(re.findall(r'[a-zA-ZÀ-ÿ]', str(name)))  # Inclure les lettres accentuées
    return unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII').lower()