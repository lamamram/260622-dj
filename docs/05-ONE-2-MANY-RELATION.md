# gestion des comptes bancaires d'un client

## consignes

* créer un lien 'Comptes' dans la nav à la place de "About"
* ce lien est lié à une url home/accounts de l'app client
* cette url est liée à une vue list_accounts
* la liste des compte doit aller chercher les comptes du client
  - on a besoin d'un model Account qui utilise une clé étrangère vers le model Client
  - doit afficher un template list_accounts.html avec la liste des comptes du client


## points pédagogiques

* One to Many relation entre Client et Account
* en deuxième intention: transforler la vue fonction en CBV: Class Based View => ListView
