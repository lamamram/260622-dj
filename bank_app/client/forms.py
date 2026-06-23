from django import forms
from .models import Client
from django.core.validators import RegexValidator

# validateur custom
MOBILE_VALIDATOR = RegexValidator(
   regex=r"^\+?[\d\s\-().]{6,20}$",
   message="Enter a valid mobile (digits, spaces, +, -, ())."
)

# Form: pour un formulaire complexe | ModelForm: pour un formulaire lié à un seul modèle
class EditClientForm(forms.ModelForm):
    class Meta:
      model = Client
      # regex email est embarquée dans le modèle
      # REM: l'attribut "fields" de la Meta, qui est une liste, n'est pas l'attribut "fields" de la classe Form
      # fields est une liste
      fields = ["email", "mobile"]
    
    # *, **: signature universelle: foncitonne avec n'importe quelle signature particulière
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       # surcharge du champs mobile avec un nouveau validator
       # self.fields est un dictionnaire
       self.fields["mobile"].validators.append(MOBILE_VALIDATOR)
