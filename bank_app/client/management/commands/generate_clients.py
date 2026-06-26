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
        # group = Group.objects.get(name="client")
        group, _ = Group.objects.get_or_create(name="client")
        print(group.name)

        fake = Faker("fr_FR")

        # for _ in range(number):
        self._create_client(fake, group)
    
    def _create_client(self, fake: Faker, group: Group):
        firstname = fake.first_name()
        lastname = fake.last_name()
        username = fake.unique.user_name()
        password  = "password"
        email = fake.unique.email()

        # Truc.objects est le Manager du modèle
        user = User.objects.create_user(
            username, 
            email, 
            password,
            first_name=firstname,
            last_name=lastname
        )
        # ajouter le nouvel utilisateur au groupe client
        user.groups.add(group)
