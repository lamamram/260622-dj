# usage simple du MVT

## création d'un 1er modèle Client:

1. classe dans `./models.py`
2. mettre en cohérence la représentation en logique serveur (modeèles django) et la base de données (tables)
  - `uv run python manage.py makemigrations` => crée un fichier de migration dans le dossier `./migrations` de l'application
  - `uv run python manage.py migrate` => applique les migrations à la base de données

## afficher le premier client dans la page d'accueil

1. insérer un client en bdd: `INSERT INTO client_client (firstname, lastname, email, mobile) VALUES ('jean', 'Dupont', 'jdupont@example.com', '0904567824')`
   - describe avec sqlite: `PRAGMA table_info(client_client)`
   - REM avec sqlit: dans query le <backsapce> permet de voir les commandes précéentes