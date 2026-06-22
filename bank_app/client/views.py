from django.shortcuts import render

# Create your views here.
# première vue : vue-fonction
def home(request):
    # créer le sous dossier templates dans l'app client et y insérer home.html
    return render(request, "home.html")