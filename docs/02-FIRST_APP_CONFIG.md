## configuration d'une application django dans un projet django

1. créer l'application
```bash
## un projet django est composé de plusieurs applications
# première application: client
cd bank_app
uv run python ../manage.py startapp client
```

2. déclarer l'application dans les paramètres du projet et dans l'application

```python
# bank_app/settings.py
# ...
INSTALLED_APPS = [
    # ...
    ## déclaration des applications que le projet utilisent
    'bank_app.client'
]
```
```python
# bank_app/client/apps.py
# ...
# nom fait référence à l'application déclarée dans settings
name = 'bank_app.client'
# diminutif
label = 'client'
```


2. configurer le chemin vers l'application client
```python
# bank_app/urls.py
# importer include pour importer un chemin python en str à partir de la racine
from django.urls import path, include
# ...
# chemins de l'application client: chemin dans l'url, chemin python vers les urls de l'application
# ...
    path("", include("bank_app.client.urls"))
```

3. configurer les urls des VUES de l'application client
```python
# créer bank_app/client/urls.py
from django.urls import path
# "." chemin relatif à partir du fichier courant
from . import views

app_name = "client"
urlpatterns = [
    # chemin relatif à partir du radical de l'app client
    # charger la vue qui est une fonction dans le module views
    path("home", views.home)
]
```

4. créer la vue home dans le module views de l'application client
```python
# bank_app/client/views.py
# Create your views here.
# ...
# première vue : vue-fonction
def home(request):
    # créer le sous dossier templates dans l'app client et y insérer home.html
    return render(request, "home.html")
```

5. créer le template `client/templates/home.html`


6. thème de l'application


