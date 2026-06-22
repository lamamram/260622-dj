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
uv run django-admin startproject bank_app .
uv run python manage.py check
uv run python manage.py runserver
```


