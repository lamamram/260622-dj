from django.urls import path
# "." chemin relatif à partir du fichier courant
from . import views

urlpatterns = [
    # chemin relatif à partir du radical de l'app client
    # charger la vue qui est une fonction dans le module views
    path("home", views.home, name="home"),
    path("home/edit_client", views.ClientUpdateView.as_view(), name="edit_client"),
                              # class.as_view() -> function
    path("home/list_accounts", views.AccountsListView.as_view(), name="list_accounts"),
    # ------------------------<type:var> var vient d'un template
    path("home/accounts_detail/<int:pk>", views.AccountDetailView.as_view(), name="account_detail"),
]
