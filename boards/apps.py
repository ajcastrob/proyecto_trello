from django.apps import AppConfig


class BoardsConfig(AppConfig):
    name = 'boards'

    def ready(self):
        from . import signals  # noqa: F401
