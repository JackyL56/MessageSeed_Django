from django.apps import AppConfig
import os


class DatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.database'

    def ready(self):
        from . import jobs

        if os.environ.get('RUN_MAIN', None) != 'true':   # Ensures we only run this method once
            jobs.start_scheduler()
