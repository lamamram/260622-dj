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
        print(number)