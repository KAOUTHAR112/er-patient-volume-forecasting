# Changelog

## 1.1.0 — 2026-07-26

- audit du dataset fourni : 9 216 admissions sur 579 jours ;
- agrégation sécurisée sans identifiants patients ;
- exécution complète du pipeline sur un split chronologique ;
- validation de SARIMAX(1,0,1) × (1,0,1,7) comme meilleur modèle selon la MAE ;
- ajout des métriques, graphiques et prévisions validés dans `results/final/` et `figures/final/` ;
- mise à jour du README et de la documentation avec une interprétation responsable.

## 1.0.0 — 2026-07-26

- restructuration complète du dépôt ;
- suppression de LSTM et TensorFlow ;
- suppression de Holt-Winters et ETS ;
- suppression de la température simulée ;
- anonymisation du pipeline de préparation ;
- ajout des modules Python, tests et documentation GitHub ;
- correction de la prévision future afin d’utiliser le meilleur modèle statistique lorsqu’il gagne ;
- ajout d’une démonstration synthétique séparée.
