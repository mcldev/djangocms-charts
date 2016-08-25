from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models_global import ChartJsGlobalSettingsModel

class ChartsGlobalSettingsAdmin(admin.ModelAdmin):
    model = ChartJsGlobalSettingsModel
    name = _("ChartJs Global Settings")
    list_display = ('name', 'enable')

