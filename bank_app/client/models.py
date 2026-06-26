from django.db import models
from django.db.models.functions import Now
from django.contrib.auth.models import User

# modèle ==> représentation d'un objet métier qui contient des règle métier
# modèle ==> peut être traduit en structure de données (ici table relationnelle)

class Address(models.Model):
    street = models.CharField(max_length=150)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)

class Client(models.Model):
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    # lié à la contrainte d'intégrité d'unicité UNIQUE en SQL
    # ajoute une contrainte sur la regex
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    # auto_now_add: le timestamp de ce champs est établi quand un objet est inséré dans la db
    # REM default vs db_default: default est créé par Django, 
    # pour sqlite: db_default=Now() déléguer la valeur par défaut à la bdd 
    created_at = models.DateTimeField(db_default=Now())

    # relation ONE TO ONE
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    # relation MANY TO MANY
    addresses = models.ManyToManyField(Address, related_name="clients")

    def __str__(self):
        """ conversion d'un objet Client en str """
        return f"{self.firstname.capitalize()} {self.lastname.upper()}"

    # REM: diff entre attributs de classe (firstname) et d'objet (age)
    # def __init__(self, age, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.age = age
    #     self.firstname = "jean"

class Account(models.Model):
    class Type(models.TextChoices):
        CURRENT = "current","Courant"
        SAVING = "saving","Livret d'Epargne"
 
    number = models.CharField(max_length=20,unique=True)
    balance = models.DecimalField(max_digits=11,decimal_places=2)
    overdraft = models.DecimalField(max_digits=11,decimal_places=2,default=0)
    credit_rate = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    type = models.CharField(max_length=10,choices=Type.choices)
    client = models.ForeignKey(
        to=Client, 
        on_delete=models.SET_NULL, null=True,
        # => permet d'utiliser client.accounts !!! 
        related_name="accounts"
    )

## modèle Payment
# champs
# - reference: (raison sociale quand on achète - compte courant) (source ou destinataire si virement - courant/épargne) str
# - type : énumération PURCHASE ('purchase', "Achat") TRANSFER ('transfert', 'Virement')
# - value: decimal (négatif si achat, positif ou négatif si virement)
# - date:
# relations
# un payment est un compte
# un compte a plusieurs payment => un client a plusieurs payment 

class Payment(models.Model):
    class Type(models.TextChoices):
        PURCHASE = "purchase","Achat"
        TRANSFER = "transfer","Virement"

    reference = models.CharField(max_length=100) 
    type = models.CharField(max_length=10, choices=Type.choices)
    value = models.DecimalField(max_digits=11, decimal_places=2) 
    date = models.DateTimeField(db_default=Now())

    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="payments")

