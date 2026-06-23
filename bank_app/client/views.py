from django.shortcuts import render
from .models import Client

# Create your views here.
# première vue : vue-fonction
def home(request):
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