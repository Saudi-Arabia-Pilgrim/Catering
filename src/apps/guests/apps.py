from django.apps import AppConfig


class GuestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.guests"

    def ready(self):
        import apps.guests.signals