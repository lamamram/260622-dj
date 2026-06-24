from django import forms
from .models import Client
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

MOBILE_REGEX = r"^\+?[\d\s\-().]{6,20}$"
MOBILE_MSG = "Enter a valid mobile (digits, spaces, +, -, ())."

# Form: pour un formulaire complexe | ModelForm: pour un formulaire lié à un seul modèle
class EditClientForm(forms.ModelForm):
    class Meta:
      model = Client
      # champs concernés par le formulaire
      fields = ["email", "mobile"]
      # personnalisation de balise input des champs du formulaire, css, et attributs html
      widgets = {
         "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "me@example.com"}),
         "mobile": forms.TextInput(attrs={"class": "form-control", "placeholder": "+ (...) 00 00 00 00"})
      }
    

    ## validation custom
    def clean_mobile(self):
        # champs déjà nettoyé par d'autres validations en amont
        data = self.cleaned_data["mobile"]
        if not re.match(MOBILE_REGEX, data):
           raise ValidationError(MOBILE_MSG)
        return data
         
