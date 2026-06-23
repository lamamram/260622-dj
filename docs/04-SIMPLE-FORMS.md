# générer un formulaire pour un flux de CUD (Create, Update, Delete) sur un modèle métier

## définition du flux: edit_client

* qu'est ce qu'on peut changer sur le client: email, mobile
* quelles sont les contraintes de validation: 
  - email, mobile doivent être non nul (required)
  - email doit matcher une regex de type email
* quels messages de succès et d'erreur à afficher dans le template
* comportement de la page en cas de succès: redirection vers la page d'accueil avec un message de succès

* structures html

```html
<!-- Header-->
        <header class="bg-dark py-5">
            <div class="container px-5">
                <div class="row gx-5 justify-content-center">
                    <div class="col-lg-6">
                        <div class="text-center my-5">
                            <h1 class="display-5 fw-bolder text-white mb-2">Edit Your Information</h1>
                            <p class="lead text-white-50 mb-4">Update your email address and mobile number.</p>
                        </div>
                    </div>
                </div>
            </div>
        </header>
```

```html
<!-- Edit form section -->
<section class="bg-light py-5">
    <div class="container px-5 my-5">
        <div class="row gx-5 justify-content-center">
            <div class="col-lg-6">
                <div class="card">
                    <div class="card-body p-5">
                       <form method="post">
                          <div class="d-grid">
                            <button class="btn btn-primary btn-lg" type="submit">Save Changes</button>
                          </div>
                       </form>

                    </div>
                </div>
                <div class="text-center mt-3">
                    ??? redirection
                </div>
            </div>
        </div>
    </div>
</section>
```
