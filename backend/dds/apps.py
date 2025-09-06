from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DdsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dds'
    verbose_name = _('Движение денежных средств')
