from django import forms
from .models import Client


# Form: pour un formulaire complexe | ModelForm: pour un formulaire lié à un seul modèle
class EditClientForm(forms.ModelForm):
    class Meta:
      model = Client
      fields = ["email", "mobile"]