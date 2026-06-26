from django.shortcuts import render, redirect
from .models import Client, Account, Payment
from .forms import EditClientForm
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from typing import Any

import logging

logger = logging.getLogger("django")

def log_out(request: HttpRequest):
    logout(request)
    return redirect("login")


def log(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, 
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                return render(request, "login.html", {"form": form})
        else:
            return render(request, "login.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})

# Create your views here.
# première vue : vue-fonction

@login_required(login_url="/login")
def home(request: HttpRequest):
    # accès statique (pas d'instanciation: Client()), avec l'attribut .objects
    # qui contient les méthodes de requêtages sur la table
    # pk = Primary Key (clé primaire) ==> id
    # techniques de requêtages (.get(id=1), .get(pk=1), first(), all() , filter())
    # client = Client.objects.get(pk=1)

    # client lié à l'utilisateurauthentifié
    client = Client.objects.filter(user=request.user).first()
    logger.info(f"donées client :{client}")
    
    # 1. créer le sous dossier templates dans l'app client et y insérer home.html
    # 2. ajouter le contexte pour injecter les objets python dans le template
    return render(request, "home.html", context={
        # c'est la clé qui donne le nom à l'objet dans le template !!!
        "client": client
    })

@login_required(login_url="/login")
def edit_client(request: HttpRequest):
    client = Client.objects.filter(user=request.user)
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

@login_required(login_url="/login")
def list_accounts(request: HttpRequest):
    ## CAS 1: lazy loading: 2 requêtes avec Where = ~60ms
    # client = Client.objects.get(pk=1)
    # accounts = client.accounts.all() # <= .accounts vient du "related_name" de la FK du modèle
    # accounts = Account.objects.filter(client=client)
    
    ## CAS 2: 1 requête avec JOIN ~28ms
    # select_related pour les relations X -> ONE
    client = Client.objects.filter(user=request.user)
    accounts = Account.objects.select_related("client").filter(client=client)
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

class AccountsListView(LoginRequiredMixin, ListView):
    model = Account
    # attribut lié à la mixin
    login_url = "/login"
    template_name = "list_accounts.html"
    # variable caractéristique d'une liste == la collection d' accounts DONC on l'appelle accounts
    context_object_name = "accounts"

    def get_queryset(self):
        """
        méthode qui retourne la liste d'objet qu'on veut voir
        liste d'objets == queryset
        """
        # client = Client.objects.filter(user=self.request.user).first()
        # client = Client.objects.get(user_id=self.request.user.id)
        # return Account.objects.filter(client=client)

        # jointure de champs: je filtre la list de compte selon à la FK de client elle même en relation avec Account
        # en SQL : double joiture account <-> client <-> user
        return Account.objects.filter(client__user=self.request.user)

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    login_url = "/login"
    template_name = "account_detail.html"
    # variable caractéristique d'une fiche == un objet account DONC on l'appelle account
    context_object_name = "account"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        cette méthode retourne le contexte de la vue
        1/ le super retourne context["account"]
        2/ on a utilise cette méthode car on ne peut pas directement utiliser account.payments
           dans les templates car relation inverse
        3/ self.object est l'objet account de cette vue
           self.object.payments n'est pas une queryset<Payment> !!! c'est un objet de relation inverse Client.Payment.None
           pour avoir la collection: le + simple: self.object.payments.all()
           ou alors un tri
        4/ le tri selon un champs .order_by("field") ou .order_by("-field") 
        5/ utiliser la sousclasse Payment.Type dont les attributs sont des filtres naturels
        """
        # le super rapatrie l'objet account
        context = super().get_context_data(**kwargs)

        payments = self.object.payments.order_by("-date")
        logger.info(self.object.payments)

        selected_type = self.request.GET.get("type")
        if selected_type:
            payments = payments.filter(type=selected_type)

        context["selected_type"] = selected_type
        context["payment_types"] = Payment.Type.choices
        context["payments"] = payments
        return context
    


class ClientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Client
    login_url = "/login"
    form_class = EditClientForm
    template_name = "edit_client.html"
    # redirection en cas de succès
    success_url = reverse_lazy("home")
    # champs injecté à partir de la Mixin qui gère les messages Flash pour les CBV
    success_message = 'List successfully saved!!!!'
    # ici on a pas d'identifiant venant de l'url et pas d'authentification
    # context_object_name = 'client'

    def get_object(self, queryset = ...):
        """
        méthode caractéristique d'une vue qui a besoin d'un objet
        ici surcharge: comportement arbitraire
        """
        return Client.objects.filter(user=self.request.user).first()