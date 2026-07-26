# Résultats de l’exécution finale

## Provenance

Ces résultats ont été recalculés à partir du fichier `Hospital ER_Data.csv` fourni pour le projet. Le fichier brut n’est pas distribué dans ce dépôt. Seule son agrégation journalière locale a été utilisée pour l’entraînement.

## Configuration

- 9 216 admissions ;
- 579 jours, du 1er avril 2023 au 30 octobre 2024 ;
- 551 observations utilisables après création des retards et fenêtres mobiles ;
- 440 observations d’entraînement ;
- 111 observations de test chronologique ;
- 40 variables explicatives ;
- horizon final : 30 jours.

## Meilleur modèle

**SARIMAX(1,0,1) × (1,0,1,7)** :

- MAE : **2,908 patients** ;
- RMSE : **3,717 patients** ;
- MAPE : **19,96 %** ;
- sMAPE : **18,34 %** ;
- R² : **0,028** ;
- précision opérationnelle ±2 : **43,2 %**.

## Comparaison avec les baselines

La moyenne naïve obtient une MAE de 2,963 et une précision ±2 de 44,1 %. Le SARIMAX améliore la MAE d’environ **1,9 %**, mais n’améliore pas la précision ±2. Le choix du meilleur modèle repose donc sur la MAE, pas sur une supériorité générale sur toutes les métriques.

## Validation temporelle des modèles d’ensemble

| Modèle | MAE CV moyenne | Écart-type MAE | RMSE CV moyenne |
|---|---:|---:|---:|
| Random Forest | 3,067 | 0,165 | 3,852 |
| Extra Trees | 3,100 | 0,188 | 3,901 |
| Gradient Boosting | 3,214 | 0,125 | 4,033 |

## Prévision des 30 jours suivants

La prévision couvre le 31 octobre au 29 novembre 2024 :

- moyenne : **16,08 admissions/jour** ;
- minimum : **15,31** ;
- maximum : **16,71**.

Ces valeurs relativement resserrées reflètent la faible dynamique explicable de la série. Elles ne constituent pas un intervalle de confiance et ne doivent pas être interprétées comme une garantie opérationnelle.

## Interprétation responsable

Le faible R² signifie que le modèle explique peu la variation quotidienne autour de la moyenne. Le résultat peut soutenir une estimation de charge globale, mais il ne permet pas d’anticiper précisément les pics journaliers. Des variables externes fiables — météo réelle, événements, épidémies, jours spéciaux ou capacités — seraient nécessaires pour tenter d’améliorer la prévision.

## Fichiers

- `results/final/model_comparison.csv` ;
- `results/final/timeseries_cv_summary.csv` ;
- `results/final/future_forecast.csv` ;
- `results/final/run_metadata.json` ;
- `figures/final/`.
