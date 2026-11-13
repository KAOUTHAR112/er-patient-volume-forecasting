# Méthodologie

## 1. Formulation

La cible est le nombre d'admissions aux urgences par jour. Le problème est traité comme une régression de série temporelle avec validation chronologique.

## 2. Agrégation et confidentialité

Le fichier patient brut est transformé en une série à deux colonnes : `Date` et `patients`. Les identifiants, noms, données démographiques et informations individuelles ne sont jamais nécessaires à la prévision du volume global.

## 3. Continuité temporelle

Toutes les dates entre le minimum et le maximum sont reconstituées. Les jours absents sont remplis avec zéro. Cette hypothèse doit être vérifiée : une date absente peut aussi représenter un défaut de collecte.

## 4. Variables explicatives

- jour, mois, année, trimestre et semaine ISO ;
- week-end ;
- encodages cycliques sin/cos ;
- jours fériés marocains ;
- retards : 1, 2, 3, 7, 14, 21 et 28 jours ;
- moyennes, écarts-types, minima et maxima mobiles : 3, 7, 14 et 28 jours ;
- différences retardées.

Toutes les statistiques mobiles sont calculées sur `target.shift(1)`, ce qui empêche l'utilisation de la valeur courante dans ses propres prédicteurs.

## 5. Split

Les 80 % premières observations forment l'entraînement et les 20 % dernières le test. Aucun mélange aléatoire n'est effectué.

## 6. Familles de modèles

### Baselines

Elles permettent de vérifier qu'un modèle complexe améliore réellement une règle simple.

### ARIMA/SARIMAX

ARIMA modélise l'autocorrélation et la différenciation. SARIMAX ajoute une composante saisonnière hebdomadaire de période 7.

### Machine Learning

Les modèles exploitent les variables calendaires, retardées et mobiles. Les modèles nécessitant une mise à l'échelle sont placés dans une `Pipeline` avec imputation médiane et standardisation.

## 7. Modèles volontairement exclus

LSTM, TensorFlow, Holt-Winters et ETS sont absents du code, du notebook et des dépendances.

## 8. Métriques

- **MAE :** erreur absolue moyenne en patients ;
- **RMSE :** pénalise davantage les grandes erreurs ;
- **MAPE/sMAPE :** erreurs relatives ;
- **R² :** part de variance expliquée ;
- **Accuracy ±2 :** proportion de jours où l'erreur absolue ne dépasse pas deux patients.

## 9. Validation temporelle

Random Forest, Extra Trees et Gradient Boosting sont également évalués avec `TimeSeriesSplit` en cinq plis. Chaque validation utilise uniquement des données antérieures à sa période de validation.

## 10. Prévision future

- meilleur modèle statistique : réentraînement sur toute la série puis prévision directe ;
- meilleur modèle ML : prévision récursive, les prédictions précédentes alimentant les retards futurs.

La prévision récursive peut accumuler les erreurs ; cette limite doit être signalée.
