# installation d'un projet django moderne


## installation et usage de uv au delà de pip et venv

* `https://docs.astral.sh/uv/`

1. téléchargement windows
  -  `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

2. générer l'nevironnement du projet: pyproject.toml, etc...
  - `uv init .` ou `uv init <project_dir_to_create>`

3. installer des outils de développement: ex. sqlit-tui
  - `uv tool install sqlit-tui`
  - REM: tool non lié à l'environnement du projet, mais à l'utilisateur
  - REM: sqlit ne veut pas dire sqlite, il permet de gérer différentes bases relationnelles

4. ajouter des dépendances et créer l'environnement du projet
```bash
## chercher les dépendances existantes de pip (legacy)
uv add -r requirements.txt
## ajouter des deps de pour développement et / ou de production
uv add --group dev django-debug-toolbar pytest-django
uv add --group prod gunicorn
## synchroniser les dépendances de l'environnement demandé (par défaut dev)
uv sync --project .
```

5. lancer le projet et piloter python avec uv

```bash
# créer le projet django dans le répertoire courant
uv run django-admin startproject bank_app .
# vérifier l'installation
uv run python manage.py check
# lancer le serveur de développement
uv run python manage.py runserver


## au cas où la base de données est corrompue
# supprimer le fichier db.sqlite3
# makemigrations => création les fichiers de migration et créer la base de données s'il n'existe pas (RAZ)
uv run python manage.py makemigrations

# lancer une première migration => création de tables dans la base de données
# Par défaut; django utilise sqlite3, et utilise des tables auth_user, auth_group, etc... pour gérer les utilisateurs et les groupes d'utilisateurs
uv run python manage.py migrate 

# ajouter une utilisateur admin: admin / me@example.com / roottoor
uv run python manage.py createsuperuser

# lancer le serveur de développement
# demander l'url http://127.0.1:8000/admin/ pour accéder à l'interface d'administration de django
```

## utilisation de sqlit-tui pour gérer la base de données sqlite3

```bash
sqlit
# taper n => créer une nouvelle connexion
# choisir le nom, le type, le chemin vers le fichier db.sqlite3

# cliquer sur le cnx
# voir les tables, les colonnes, les données, etc...

# requêter: dans query
# à la sauce vim: taper i pour mode insertion
# ensuite taper la requête sql, ex: select * from auth_user;
# taper ESC pour sortir du mode insertion
# taper entrée pour exécuter la requête
```

## usages avec git

```bash
# ajouter un fichier .bash_profile dans votre dossier utilisateur
test -f ~/.bashrc && source ~/.bashrc
```

```bash
# ajouter un fichier .bashrc dans votre dossier utilisateur
alias sync='git checkout main && git pull && git checkout -'
alias override='git checkout main && git pull && git checkout - && git merge -X theirs main'
```

