# Audit du dataset fourni

## Résumé vérifié

| Élément | Valeur |
|---|---:|
| Lignes | 9 216 |
| Colonnes | 12 |
| Identifiants patients distincts | 9 216 |
| Dates invalides | 0 |
| Lignes dupliquées | 0 |
| Première admission | 1er avril 2023 à 01:13 |
| Dernière admission | 30 octobre 2024 à 23:44 |
| Jours après agrégation | 579 |
| Volume quotidien minimum | 7 |
| Volume quotidien médian | 16 |
| Volume quotidien moyen | 15,92 |
| Volume quotidien maximum | 30 |

## Colonnes sensibles

Le fichier contient notamment :

- `Patient Id` ;
- `Patient First Inital` ;
- `Patient Last Name` ;
- date et heure individuelles d’admission ;
- âge, sexe et origine déclarée.

Ces informations ne sont pas nécessaires pour prévoir le volume journalier et ne sont jamais copiées vers les résultats publics.

## Valeurs manquantes détectées

- `Department Referral` : 5 400 valeurs manquantes ;
- `Patient Satisfaction Score` : 6 699 valeurs manquantes ;
- autres colonnes : aucune valeur manquante détectée.

Ces colonnes ne sont pas utilisées dans le pipeline final, car la cible est uniquement le nombre quotidien d’admissions.

## Donnée publique retenue

Le pipeline produit localement une table à deux colonnes :

```csv
Date,patients
2023-04-01,19
2023-04-02,13
```

Même cette table agrégée n’est pas incluse automatiquement dans GitHub tant que la licence et l’autorisation de redistribution de la source ne sont pas confirmées.
