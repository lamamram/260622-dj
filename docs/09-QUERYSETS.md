# QuerySet & expressions F

## 1. Les QuerySet

### Qu'est-ce qu'un QuerySet ?

Un **QuerySet** est une représentation Python d'une requête sur la base de
données. On le construit à partir du `Manager` du modèle (`Model.objects`) :

```python
Account.objects.all()                  # tous les comptes
Account.objects.filter(type="saving")  # les livrets
Account.objects.get(pk=1)              # UN compte (erreur si 0 ou plusieurs)
```

* les querysets sont **chaînables** : chaque `filter()` / `exclude()` / `order_by()` renvoie un
  **nouveau** QuerySet.

```python
# rien n'est exécuté ici : juste une requête construite progressivement
qs = Account.objects.filter(type="current").exclude(balance=0).order_by("-balance")

# SQL exécuté seulement maintenant
for account in qs:
    ...
```

### Les lookups de champ : la syntaxe `champ__lookup`

Pour filtrer autrement que sur l'égalité stricte, on suffixe le nom du champ
par `__` (double underscore) suivi d'un **lookup** :

```python
Account.objects.filter(balance__gt=1000)        # balance > 1000
Account.objects.filter(balance__gte=1000)       # >=
Account.objects.filter(balance__lt=0)           # < 0
Account.objects.filter(number__startswith="FR") # commence par "FR"
Account.objects.filter(type__in=["current", "saving"])
Client.objects.filter(lastname__icontains="dup") # contient, insensible à la casse
```

Lookups fréquents : `exact` (défaut), `gt`/`gte`/`lt`/`lte`, `in`,
`contains`/`icontains`, `startswith`/`endswith`, `isnull`, `range`.

Sur les dates, on accède aux composantes avec le même mécanisme :

```python
Payment.objects.filter(date__year=2026)
Payment.objects.filter(date__month=6)
Payment.objects.filter(date__year=2026, date__month=6)  # juin 2026
```

### Traverser les relations avec `__`

C'est le point clé : **le même `__` sert à « sauter » d'un modèle à un autre**
en suivant une `ForeignKey`, une `OneToOneField` ou une relation inverse.

Rappel des relations du projet :

```
Account.client  -> ForeignKey vers Client  (Account -> Client)
Client.user  -> OneToOneField vers User (Client -> User)
Account <- payments -> relation inverse (related_name="payments")
```

On enchaîne les sauts dans le `filter()` :

```python
# comptes dont le client a pour email "x@y.fr"
Account.objects.filter(client__email="x@y.fr")

# comptes du client lié à l'utilisateur connecté
#   Account --client--> Client --user--> User
Account.objects.filter(client__user=request.user)

# clients ayant au moins un ACHAT (relation inverse payments)
Client.objects.filter(payments__type="purchase")
```

> `client__user` se lit de gauche à droite :
> « le champ `client` de `Account`, puis le champ `user` de ce `Client` ».
> Chaque `__` = une jointure SQL.

On peut **combiner** traversée de relation et lookup de champ dans la même
expression :

```python
# achats (payments.type) du mois de juin 2026 (payments.date)
Client.objects.filter(
    payments__type="purchase",
    payments__date__year=2026,    # relation payments → champ date → lookup year
    payments__date__month=6,
)
```

### Exemple du projet : filtrer une ListView (CBV)

Dans `bank_app/client/views.py`, `AccountsListView` ne montre que les comptes
du client lié à l'utilisateur connecté, via une seule traversée de relations :

```python
class AccountsListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = "list_accounts.html"
    context_object_name = "accounts"

    def get_queryset(self):
        # traverse la FK Account -> Client puis la OneToOne Client -> user
        # => une seule requête avec jointure
        return super().get_queryset().filter(client__user=self.request.user)
```

> Alternative plus lourde : `filter(client=Client.objects.filter(user=...))`
> génère une **sous-requête** `WHERE client_id IN (SELECT ...)`.
> `client__user=...` fait directement la **jointure** : plus simple, plus rapide.

### Charger les relations efficacement : `select_related` / `prefetch_related`

Pour éviter le problème des « N+1 requêtes » quand on accède aux relations :

```python
# X -> 1 (FK / OneToOne) : JOIN, 1 requête
Account.objects.select_related("client")

# X -> N (relation inverse / ManyToMany) : 2 requêtes batchées (WHERE ... IN)
Client.objects.prefetch_related("accounts")
```


## 2. Les expressions F

### Le problème qu'elles résolvent

Sans `F`, pour calculer à partir d'un champ il faut **ramener l'objet en
Python**, le modifier, puis le sauvegarder :

```python
# 2 requêtes + condition de course possible
account = Account.objects.get(pk=1)
account.balance = account.balance + 100   # calcul en Python
account.save()
```

Avec `F`, le calcul est exprimé **directement en SQL**, exécuté par la base de
données, sans charger l'objet :

```python
from django.db.models import F

# UPDATE ... SET balance = balance + 100 (1 requête, atomique)
Account.objects.filter(pk=1).update(balance=F("balance") + 100)
```

`F("nom_du_champ")` est une **référence au champ côté base** : « la valeur de
ce champ, pour chaque ligne, telle qu'elle est en base ». Et — comme pour les
lookups — `F` accepte aussi la traversée de relations : `F("payments__value")`,
`F("accounts__balance")`.

### Cas 1 — comparer/combiner deux champs entre eux

```python
from django.db.models import F

# comptes dont le solde dépasse le découvert autorisé
Account.objects.filter(balance__gt=F("overdraft"))

# annoter chaque compte avec son solde disponible (balance + overdraft)
Account.objects.annotate(dispo=F("balance") + F("overdraft"))
```

### Cas 2 — F dans une agrégation

**Meilleur acheteur du mois** — les achats sont stockés en valeur **négative** ;
`-F("payments__value")` les ré-exprime en montant **positif** côté base :

```python
from django.db.models import Sum, F

top_buyer = (
    Client.objects
    .filter(
        payments__type=Payment.Type.PURCHASE,
        payments__date__year=2026,
        payments__date__month=6,
    )
    .annotate(total_achats=Sum(-F("payments__value")))  # SUM(-value)
    .order_by("-total_achats")
    .first()
)
```

**Fonds disponibles par client** — `F` combine deux champs, le tout sommé sur
tous les comptes du client :

```python
top_funds = (
    Client.objects
    .annotate(
        solde_disponible=Sum(F("accounts__balance") + F("accounts__overdraft"))
    )  # SUM(balance + overdraft)
    .order_by("-solde_disponible")
    .first()
)
```

### Pourquoi utiliser F ?

* **Performance** : un seul aller-retour SQL, pas de boucle Python sur les lignes.
* **Atomicité** : `update(x=F("x") + 1)` évite les conditions de course (deux
  requêtes simultanées ne s'écrasent pas).
* **Expressivité** : on décrit le calcul, la base l'exécute.