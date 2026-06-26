# commande Django utilisant Faker

## but

* générer des clients avec leur utilisateurs
* //      des comptes utilisateurs de groupe client pour les clients
* //      des payments pour les comptes

> générer un nb de client en paramètre, avec un compte courant (overdraft 200 ou 1000) et un livret et pour chaque compte, générer < 10 payments

## générer des valeurs de champs avec Faker

### user

- username: `faker.user_name()`
- email: `faker.email()`
- password: "password"
- first_name: `faker.first_name()`
- last_name: `faker.last_name()`

### client

- firstname
- lastname
- email
- mobile: `faker.phone_number()`
- user = user

### account : règles selon le type de compte

- number: ??? 
- balance: `faker.pydecimal()`
- overdraft: ??? <- random
- credit_rate: `faker.pydecimal()`  intervalle [0 - 10]
- type: déjà l'enumération (Type)
- client = client

### payment: règle selon le type de compte et du type de payment

- type: déjà l'enumération (Type)
- reference: entrepise ou personne
- value: +- fake.pydecimal()  intervalle [0 - 1000]
- date: `faker.date_time_this_year()`
- account = account

## créer une commande Django

1. créer un package management et un sous-package commands dans l'app client

2. créer un fichier `generate_clients.py` dans le sous-package commands

```python
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from faker import Faker
# pour le décorateur transaction.atomic
from django.db import transaction
## les modèles


class Command(BaseCommand):
    help=(
        """générer un nb de client en paramètre, avec un compte courant (overdraft 200 ou 1000) et un livret et pour chaque compte, générer < 10 payments"""
    )

    def add_arguments(self, parser):
        """
        gérer le paramètres à la sauce argparse
        """
        parser.add_argument(
            "number",
            type=int,
            help="Nombre de clients à générer.",
        )
    @transaction.atomic
    def handle(self, *args, **options):
        number = options["number"]
        # ???
```

### éléments de django

* les modèles User et Group pour créer les utilisateur de groupe client
  - https://docs.djangoproject.com/en/6.0/ref/contrib/auth/
* créer (et insérer dans la bd) les autres modèles à partir d'objets Client.objects.???
* exécuter command : `python manage.py ma_commande ?`

#### créer un objet en django

* créer un modèle python (sans référence à un enregistrement de table)
  - user = User(firstname=f, lastname=l, ...)
  - dans ce cas il nous faut faire user.save() pour synchroniser

* créer le modèle avec réf à la table
  - user = User.objects.create_user(...)

#### gestion des transaction

* `transaction.atomic` ==> tout est ok ou ERROR
* `transaction.non_atomic_requests` ==> je peux commiter et rollback ce que je veux 
* en sqlite: gestion des transaction  est hasardeuse: mieux raise une erreur