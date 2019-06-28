from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'api'

    def ready(self):
        import api.signals
