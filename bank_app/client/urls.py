from django.urls import path
# "." chemin relatif à partir du fichier courant
from . import views

app_name = "client"
urlpatterns = [
    # chemin relatif à partir du radical de l'app client
    # charger la vue qui est une fonction dans le module views
    path("home", views.home)
]
