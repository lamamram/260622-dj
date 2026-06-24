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
    else:
        form = EditClientForm(instance=client)
    return render(request, "edit_client.html", {"form": form})


    # si on vient de la page d'accueil

def list_accounts(request: HttpRequest):
    client = Client.objects.first()
    accounts = Account.objects.filter(client=client)
    return render(request, "list_accounts.html", {"accounts": accounts})
