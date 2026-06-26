from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from faker import Faker
from bank_app.client.models import Client, Account, Payment
# pour le décorateur transaction.atomic
from django.db import transaction
import random
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
        # group = Group.objects.get(name="client")
        group, _ = Group.objects.get_or_create(name="client")

        fake = Faker("fr_FR")

        for _ in range(number):
           client = self._create_client(fake, group)
           self._create_accounts(fake, client)

        print("TERMINADO")
        # raise ValueError("test")

    def _create_client(self, fake: Faker, group: Group) -> Client:
        user_obj = dict(
          first_name = fake.first_name(),
          last_name = fake.last_name(),
          username = fake.unique.user_name(),
          password  = "password",
          email = fake.unique.email(),
        )
        # print(user_obj)


        # Truc.objects est le Manager du modèle qui synchronise avec la bdd
        user = User.objects.create_user(**user_obj)
        # ajouter le nouvel utilisateur au groupe client
        user.groups.add(group)

        client_obj = {
            "firstname": user_obj["first_name"],
            "lastname": user_obj["last_name"],
            "email": user_obj["email"],
            "mobile": fake.phone_number(),
            "user": user
        }
        return Client.objects.create(**client_obj)
    
    def _create_accounts(self, fake: Faker, client: Client):
        current = Account.objects.create(
            number=fake.unique.iban(),
            balance=fake.pydecimal(right_digits=2, min_value=0, max_value=9999),
            overdraft=random.choice([200, 1000]),
            credit_rate=0,
            type=Account.Type.CURRENT,
            client=client,
        )

        # livret : solde < 23000
        saving = Account.objects.create(
            number=fake.unique.iban(),
            balance=fake.pydecimal(right_digits=2, min_value=0, max_value=22999),
            overdraft=0,
            credit_rate=random.choice([1.5, 2.25, 4]),
            type=Account.Type.SAVING,
            client=client,
        )

        self._create_payments(fake, current, allow_purchase=True)
        # pas d'achat sur un livret : virements uniquement
        self._create_payments(fake, saving, allow_purchase=False)

    def _create_payments(self, fake: Faker, account: Account, allow_purchase: bool):
        # moins de 10 paiements par compte
        for _ in range(random.randint(1, 9)):
            if allow_purchase and random.random() < 0.7:
                # achat : référence = raison sociale d'entreprise, montant négatif
                Payment.objects.create(
                    type=Payment.Type.PURCHASE,
                    reference=fake.company(),
                    value=-fake.pydecimal(left_digits=3, right_digits=2, positive=True),
                    date=fake.date_this_year(before_today=True),
                    account=account
                )
            else:
                # virement : référence = prénom + nom, montant positif ou négatif
                Payment.objects.create(
                    type=Payment.Type.TRANSFER,
                    reference=fake.name(),
                    value=fake.pydecimal(left_digits=3, right_digits=2),
                    date=fake.date_this_year(before_today=True),
                    account=account
                )

        
        
