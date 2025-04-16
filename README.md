# Application Todo List

Une application de gestion de tâches moderne et élégante construite avec Flask.

## Fonctionnalités

- ✨ Interface utilisateur moderne et responsive
- 🌓 Mode sombre/clair
- 📋 Gestion complète des tâches (ajout, modification, suppression)
- 🏷️ Statuts des tâches (à faire, en cours, terminé)
- 🔍 Recherche de tâches
- 🔄 Filtrage et tri des tâches
- 📊 Page de statistiques

## Technologies utilisées

- Flask
- SQLAlchemy
- SQLite
- HTML/CSS
- JavaScript

## Installation locale

1. Cloner le dépôt :
```bash
git clone [URL_DU_REPO]
cd todo-app
```

2. Créer un environnement virtuel :
```bash
python -m venv .venv
source .venv/bin/activate  # Sur Unix/macOS
# ou
.venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Lancer l'application :
```bash
python app.py
```

5. Ouvrir l'application dans votre navigateur :
```
http://localhost:8080
```

## Déploiement

L'application est configurée pour être déployée sur Render.com. Pour déployer :

1. Créer un compte sur Render.com
2. Connecter votre dépôt GitHub
3. Créer un nouveau service Web
4. Sélectionner le dépôt
5. Laisser Render utiliser les configurations du fichier `render.yaml`

## Licence

MIT 