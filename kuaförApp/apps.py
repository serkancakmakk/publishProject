from django.apps import AppConfig


class KuaförappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kuaförApp"
    def ready(self):
        import kuaförApp.signals
        print('Sinyhaller yüklendi') 
