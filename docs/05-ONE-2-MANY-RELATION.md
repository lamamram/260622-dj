# gestion des comptes bancaires d'un client

## consignes

* créer un lien 'Comptes' dans la nav à la place de "About"
* ce lien est lié à une url home/accounts de l'app client
* cette url est liée à une vue list_accounts
* la liste des compte doit aller chercher les comptes du client
  - on a besoin d'un model Account qui utilise une clé étrangère vers le model Client
  - doit afficher un template list_accounts.html avec la liste des comptes du client


## points pédagogiques

* One to Many relation entre Client et Account
* en deuxième intention: transforler la vue fonction en CBV: Class Based View => ListView

## model Account

* points intéressants:
  - type DecimalField
  - Pas de type natif pour les chaine de caractères fixes => CHAR
  - faire une énumération avec une sous classe héritée de `TextChoices` pour le type de compte (courant, épargne, etc.)

* le champs "client" fait une relation Many to One avec le model Client
  - clé étrangère vers le model Client `ForeignKey`
  - `on_delete=models.CASCADE` pour supprimer les comptes si le client est supprimé
  - `on_delete=models.SET_NULL` + `nul=True` pour préserver les comptes si le client est supprimé
  - génère un champs `client_id` dans la table account

* relation réciproque
  - `related_name='accounts'` pour accéder aux comptes d'un client via `client.accounts.all()`
  - `related_query_name='account'` pour filtrer les clients selon leurs comptes via `Client.objects.filter(account__type=Account.Type.COURANT)`

* Lazy/Eager loading
  - par défaut, django ne charge pas les relations, en créant l'objet client
  - en demandant tous les comptes d'un client, django va lancer une requête SQL pour aller chercher les comptes
  - dans une boucle for, on aura autant de requêtes SQL que d'itérations => problème de performance

  ```python
  client = Client.objects.get(pk=1) # 1 requête
  accounts = client.accounts.all()  # lazy loading : requête(s)
  # ...
  # client.Client.objects.select_related('accounts').all()  # eager loading : 1 requête avec les relations 
  ```

## vue list_accounts

* filtrer les comptes selon le client connecté
```python
client=Client.objects.get(pk=1)
Accounts.objects.filter(client=client)
```

## templates / lien (déjà vu) 

