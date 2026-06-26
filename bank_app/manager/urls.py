from django.urls import path
# "." chemin relatif à partir du fichier courant
from . import views

urlpatterns = [
    path("logout", views.log_out, name="m_logout"),
    path("login", views.log, name="m_login"),
    path("home", views.home, name="m_home"),
]
