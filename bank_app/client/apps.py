from django.apps import AppConfig


class ClientConfig(AppConfig):
    # nom fait référence à l'application déclarée dans settings
    name = 'bank_app.client'
    # diminutif
    label = 'client'
