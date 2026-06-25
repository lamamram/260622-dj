# construction d'une authentification basique avec Django

## 1. créer les groupes / users / permissions

* `admin/`: superuser

## 2. créer la page de login

* `login.html` : page de login
* `base_auth.html` : page de base pour l'authentification (pas de nav)
* utiliser un formulaire pour gérer les erreurs de login (username/password invalides)

## 3. créer l'url de login

* RAD

## 4. créer la vue de login

```
si soumet le formulaire de login:
    si le formulaire est valide:
        récupérer le username et le password
        authentifier l'utilisateur
      si username/password valides:
        connecter l'utilisateur
        rediriger vers la page d'accueil
      sinon:
        retourner la page de login avec les messages d'erreur
    sinon:
        retourner la page de login avec les messages d'erreur
sinon:
    je consulte la page de login avec un formulaire vide
```

## 5. gérer l'authentification dans les vues

1. pour les vues fonction => le décorateur `@login_required` (avec `login_url` si besoin) pour rediriger vers la page de login si l'utilisateur n'est pas connecté

2. pour les vues basées sur les classes => le mixin `LoginRequiredMixin` (avec `login_url` si besoin) idem

3. rediriger la page de login si l'utilisateur est déjà connecté (ex: page de login, page d'inscription, ...)
