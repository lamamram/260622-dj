from django.urls import path
# "." chemin relatif à partir du fichier courant
from . import views

urlpatterns = [
    # chemin relatif à partir du radical de l'app client
    # charger la vue qui est une fonction dans le module views
    path("home", views.home, name="home"),
    path("home/edit_client", views.edit_client, name="edit_client"),
    path("home/list_accounts", views.list_accounts, name="list_accounts")
]
