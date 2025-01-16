# README

## Guide Utilisateur

### Prérequis

Pour déployer et exécuter ce tableau de bord, vous devez disposer des éléments suivants :

* Python 3.8 ou une version ultérieure installé sur votre machine
* `<span>pip</span>` (gestionnaire de packages Python)
* Les bibliothèques Python requises listées dans le fichier `<span>requirements.txt</span>`

### Installation et Déploiement

1. Clonez le dépôt :
   ```
   git clone <repository-url>
   cd <repository-name>
   ```
2. Créez et activez un environnement virtuel :
   ```
   python -m venv venv
   source venv/bin/activate  # Sous Windows : venv\Scripts\activate
   ```
3. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```
4. Lancez l'application :
   ```
   python main.py
   ```
5. Ouvrez votre navigateur et accédez à l'adresse :
   ```
   http://localhost:7999
   ```

### Utilisation

Une fois déployé, vous pouvez :

* Sélectionner une ville à l'aide du menu déroulant pour afficher des visualisations spécifiques.
* Explorer des graphiques tels que des diagrammes circulaires, des histogrammes, des cartes thermiques, etc.
* Analyser les données sociales et économiques des municipalités d'Île-de-France.

---

## Données

### Sources

Le tableau de bord utilise des données nettoyées et normalisées extraites de :

1. Données salariales : [https://www.insee.fr/fr/statistiques/fichier/5055909/BASE_TD_FILO]()
2. Données des communes d'IDF : [https://www.data.gouv.fr/fr/datasets/r/91c0bdc4-0a5b-4ac8-950e-64a1ec207957]()

### Téléchargement

* Executer le script `<span>get_data.py</span> `
* Executer le script `<span>clean_data.py</span>`

### Description

Les données incluent :

* Le statut d'activité de la population (actifs, inactifs, retraités)
* Les échelles de salaires et les salaires médians.
* Les indices de Gini pour analyser les inégalités économiques.

### Prétraitement

Les scripts de nettoyage et de normalisation des données se trouvent dans le répertoire `<span>utils</span>` :

* `<span>clean_data.py</span>` : Nettoie les fichiers de données brutes.
* `<span>normalise_name.py</span>` : Normalise les noms des villes pour assurer la cohérence.
* `<span>get_data.py</span>` : Télécharge les données brutes si elles sont manquantes.

---

## Guide du Développeur

### Architecture

Le projet suit une architecture modulaire :

* **Composants** : Situés dans `<span>src/components</span>`. Chaque composant (par exemple, diagramme circulaire, graphique en barres) dispose de son propre fichier pour une meilleure modularité.
* **Utilitaires** : Situés dans `<span>utils</span>`. Contient les scripts pour le nettoyage, le téléchargement et la normalisation des données.
* **Application Principale** : Le point d'entrée `<span>main.py</span>` initialise l'application Dash et définit la mise en page.

### Ajouter une Nouvelle Page ou un Graphique

1. Créez un nouveau fichier dans le répertoire `<span>src/components</span>` pour un nouveau graphique.
   Exemple : `<span>graph.py</span>`
2. Définissez une fonction qui prend un `<span>DataFrame</span>` en entrée et renvoie un composant Dash (par exemple, `<span>dcc.Graph</span>`).
3. Importez et intégrez votre nouveau graphique dans la mise en page de `<span>main.py</span>`.
4. Facultativement, mettez à jour la section `<span>callbacks</span>` dans `<span>main.py</span>` pour rendre votre graphique interactif.

## Rapport d'analyse

* La majorité des villes présentent un salaire médian compris entre 20 000€ et 30 000€. Cette tranche est la plus représentée, indiquant une concentration importante des revenus médians dans cette fourchette.
* Très peu de villes ont des salaires médians supérieurs à 50 000€, soulignant une disparité importante et probablement une polarisation dans certaines zones urbaines riches.
* Il semble y avoir une corrélation négative entre les indemnités de chômage et le salaire médian. Les villes avec des salaires médians bas tendent à avoir un pourcentage plus élevé d'indemnités de chômage.
* Certaines anomalies peuvent apparaître où des zones avec des salaires moyens ont des taux de chômage inattendus.
* La majorité des villes se trouvent dans une tranche où les salaires médians sont autour de 20 000€-30 000€ et les pensions/retraites représentent une part notable de leur économie.
* Les zones avec des salaires plus faibles semblent aussi avoir une proportion importante de pensions/retraites, ce qui peut indiquer un vieillissement de la population dans ces régions.

---

### **Conclusions Globales :**

1. Il existe une forte disparité entre les salaires médians, avec une majorité des villes concentrées dans des tranches modestes.
2. Les zones avec des revenus plus faibles dépendent davantage des aides sociales et des retraites, ce qui peut refléter des dynamiques socio-économiques spécifiques (par exemple, chômage élevé ou population vieillissante).
3. Ces données pourraient être utilisées pour orienter les politiques publiques en ciblant les zones économiquement vulnérables.

## Droits d'Auteur

Je déclare sur l’honneur que le code fourni a été produit par moi-même, à l’exception des lignes ci-dessous :

### Références

1. Documentation Plotly : [Lien](https://plotly.com/python/pie-charts/)
2. Documentation Dash :  [Lien](https://dash.plotly.com/)

### Explication du Code Emprunté

* Les implémentations de `<span>dcc.Graph</span>` et `<span>dcc.Dropdown</span>` sont adaptées à partir de la documentation officielle de Dash.
* La structure des fonctions de callback suit les meilleures pratiques énoncées dans le guide Dash.

### Déclaration d’Originalité

Toute ligne non déclarée ci-dessus est réputée être produite par l’auteur du projet. L’absence ou l’omission de déclaration sera considérée comme du plagiat.
