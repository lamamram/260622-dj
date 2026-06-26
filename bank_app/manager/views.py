from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from bank_app.client.models import Client, Payment
import logging

logger = logging.getLogger("django")

def manager_ns(user: User):
    is_manager = list(filter(lambda g: g.pk == 2, user.groups.all()))
    return "m_" if is_manager else ""

def log_out(request: HttpRequest):
    logout(request)
    return redirect("m_login")

def log(request: HttpRequest):
    if request.user.is_authenticated: 
        return redirect(f"{manager_ns(request.user)}home")
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if manager_ns(user):
                login(request, user)
                logger.info("ok")
                return redirect("m_home")
            return redirect("home")
        else:
            return render(request, "manager/login.html", {"form": form})
    else:
        form = AuthenticationForm(request)
        return render(request, "manager/login.html", {"form": form})

@login_required(login_url="/manager/login")
def home(request: HttpRequest):
    # Client ayant le plus acheté (en valeur) en juin 2026.
    #
    # Un achat est stocké avec une valeur NÉGATIVE (sortie d'argent).
    # F("payments__value") référence ce champ directement côté base ;
    # le préfixe "-" l'inverse pour obtenir un montant dépensé POSITIF,
    # calculé par la base de données et non en Python.
    top_buyer = (
        Client.objects
        # on ne garde que les achats du mois de juin 2026
        .filter(
            accounts__payments__type=Payment.Type.PURCHASE,
            accounts__payments__date__year=2026,
            accounts__payments__date__month=6,
        )
        # agrégation par client : somme des montants dépensés (positifs grâce au -F)
        .annotate(total_achats=Sum(-F("accounts__payments__value")))
        # le plus gros acheteur en premier
        .order_by("-total_achats")
        .first()
    )

    # Client ayant le plus de fonds disponibles.
    #
    # Le solde disponible d'un compte = balance + overdraft (marge de découvert).
    # Ici F() combine DEUX champs entre eux directement côté base :
    # Sum(F("accounts__balance") + F("accounts__overdraft")) agrège ce solde
    # sur tous les comptes du client.
    top_funds = (
        Client.objects
        .annotate(
            solde_disponible=Sum(
                F("accounts__balance") + F("accounts__overdraft")
            )
        )
        .order_by("-solde_disponible")
        .first()
    ) 

    return render(request, "manager/home.html", context={
        "user": request.user,
        "top_buyer": top_buyer,
        "top_funds": top_funds,
    })
