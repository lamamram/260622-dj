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