# Publication sur GitHub

## 1. Créer un dépôt vide

Nom conseillé :

```text
er-patient-volume-forecasting
```

Ne cochez pas l'ajout automatique d'un README si vous utilisez ce dossier déjà préparé.

## 2. Vérifier les données

```cmd
git status
```

Le fichier patient brut ne doit pas apparaître.

## 3. Premier commit

```cmd
git init
git add .
git commit -m "Initial commit: ER patient volume forecasting"
git branch -M main
```

## 4. Associer le dépôt

```cmd
git remote add origin https://github.com/KAOUTHAR112/er-patient-volume-forecasting.git
git push -u origin main
```

Si `origin already exists` :

```cmd
git remote set-url origin https://github.com/KAOUTHAR112/er-patient-volume-forecasting.git
git push -u origin main
```

Chaque commande doit être exécutée sur sa propre ligne.

## 5. Ajouter les notebooks nettoyés

Les notebooks publics doivent :

- être exécutables de haut en bas ;
- ne pas contenir de données individuelles ;
- ne pas contenir de chemins personnels Windows ;
- avoir des cellules Markdown explicatives ;
- avoir les sorties effacées avant publication si elles sont sensibles.
