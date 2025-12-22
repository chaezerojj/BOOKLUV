from django.apps import AppConfig
class KlubTalkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'klub_talk'

    def ready(self):
        import klub_talk.signals  # Signal 등록
