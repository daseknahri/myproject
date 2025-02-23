from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class RentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rent'  # This should be a plain string for the app name
    verbose_name = _('rent')  # Use lazy translation here