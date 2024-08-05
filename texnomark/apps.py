from django.apps import AppConfig


class TexnomarkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'texnomark'

    def ready(self):
        import texnomark.signals