from django.apps import AppConfig

class GestionBibliotecaConfig(AppConfig):
    name = 'gestion_biblioteca'

    def ready(self):
        import gestion_biblioteca.signals  # Importa las señales
