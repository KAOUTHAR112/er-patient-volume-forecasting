# Confidentialité et données

## Données interdites dans le dépôt public

Ne publiez jamais :

- identifiant du patient ;
- nom ou initiales ;
- date et heure d'admission individuelles ;
- âge, sexe, origine ethnique ou orientation clinique au niveau individuel ;
- fichier CSV brut ;
- captures montrant des lignes patient.

## Données autorisées

Le pipeline public utilise uniquement :

```text
Date, patients
```

Ces données agrégées réduisent fortement le risque de réidentification, mais leur publication doit tout de même respecter la politique de l'établissement et la licence de la source.

## Commande recommandée

```bash
python prepare_data.py --input "chemin/privé/Hospital ER_Data.csv"
```

Le script écrit le fichier agrégé dans `data/processed/`, dossier ignoré par Git à l'exception de sa documentation.

## Vérification avant chaque push

```bash
git status
git diff --cached
```

Recherchez notamment les extensions `.csv`, `.xlsx`, `.parquet` et les notebooks contenant des sorties.
