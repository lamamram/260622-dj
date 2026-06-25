from django.shortcuts import render, redirect
from .models import Client, Account
from .forms import EditClientForm
from django.http import HttpRequest
from django.contrib import messages

# Create your views here.
# première vue : vue-fonction
def home(request: HttpRequest):
    # accès statique (pas d'instanciation) avec l'attribut .objects
    # qui contient les méthodes de requêtages sur la table
    # pk = Primary Key (clé primaire) ==> id
    # techniques de requêtages (.get(id=1), .get(pk=1), first(), all() , filter())
    client = Client.objects.get(pk=1)
    # 1. créer le sous dossier templates dans l'app client et y insérer home.html
    # 2. ajouter le contexte pour injecter les objets python dans le template
    return render(request, "home.html", context={
        # c'est la clé qui donne le nom à l'objet dans le template !!!
        "client": client
    })

def edit_client(request: HttpRequest):
    client = Client.objects.get(pk=1)
    # si le formulaire est validé (requête HTTP POST/PUT/PATCH)
    if request.method == "POST":
        form = EditClientForm(
            # données insérés par le client dans le formulaire
            data=request.POST,
            instance=client
        )
        if form.is_valid():
            # mettre à jour les données du modèle client à partir
            # des données du formulaire
            form.save()
            messages.success(request, "données mises à jour !")
            # rediriger vers la page d'accueil
            return redirect(to="home")
        else:
            messages.error(request, "checker les erreurs ci-dessous")
    # méthode HTTP GET
    else:
        form = EditClientForm(instance=client)
    return render(request, "edit_client.html", {"form": form})

def list_accounts(request: HttpRequest):
    ## CAS 1: lazy loading: 2 requêtes avec Where = ~60ms
    # client = Client.objects.get(pk=1)
    # accounts = client.accounts.all() # <= .accounts vient du "related_name" de la FK du modèle
    # accounts = Account.objects.filter(client=client)
    
    ## CAS 2: 1 requête avec JOIN ~28ms
    # select_related pour les relations X -> ONE
    accounts = Account.objects.select_related("client").filter(client_id=1)

    ## CAS 3: 2 requêtes mais batchées avec Where IN => ~60ms
    # prefetch_related pour les relation X -> MANY
    # client = Client.objects.prefetch_related("accounts").get(pk=1) # 2 requêtes batchées
    # accounts = client.accounts.all() # <= pas de requêtes
    
    ## CONCLUSION: avec un seul objet qui va chercher ses relations 
    # ==> object.[select|prefetch].get(...)
    # ==> jointure SQL
    # ==> plus rapide

    ## REM: avec beaucoup de client et leurs comptes
    # ==> CAS 3: car eager_loading sur la première instruction Client.objects.prefetch...
    # ==> 2 requêtes avec IN mieux que = dans ce cas là

    
    return render(request, "list_accounts.html", {"accounts": accounts})
