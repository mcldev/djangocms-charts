from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from .forms import GlobalOptionsInlineForm, ChartOptionsInlineForm, DatasetOptionsInlineForm, AxisOptionsInlineForm
from .models import GlobalOptionsGroupModel, GlobalOptionsModel, \
    ChartOptionsGroupModel, ChartOptionsModel,\
    DatasetOptionsGroupModel, DatasetOptionsModel, \
    AxisOptionsGroupModel, AxisOptionsModel


# Inline Forms for Options
# ------------------------
from .models_axes import AxisModel


class OptionsInlineBase(admin.TabularInline):
    fields = ['label', 'type', 'value']
    list_display = ('label', 'type', 'value')
    extra = 0


class GlobalOptionsInlineAdmin(OptionsInlineBase):
    model = GlobalOptionsModel
    form = GlobalOptionsInlineForm

class ChartOptionsInlineAdmin(OptionsInlineBase):
    model = ChartOptionsModel
    form = ChartOptionsInlineForm

class DatasetOptionsInlineAdmin(OptionsInlineBase):
    model = DatasetOptionsModel
    form = DatasetOptionsInlineForm

class AxisOptionsInlineAdmin(OptionsInlineBase):
    model = AxisOptionsModel
    form = AxisOptionsInlineForm


# Register Options Groups
# ------------------------
@admin.register(GlobalOptionsGroupModel)
class GlobalOptionsAdmin(admin.ModelAdmin):
    fields = ['name', 'enabled', 'site' ]
    list_display = ('name', 'enabled')
    inlines = [
        GlobalOptionsInlineAdmin,
    ]

@admin.register(ChartOptionsGroupModel)
class DatasetOptionsAdmin(admin.ModelAdmin):
    fields = ['name', ]
    list_display = ('name',)
    inlines = [
        ChartOptionsInlineAdmin,
    ]

@admin.register(DatasetOptionsGroupModel)
class DatasetOptionsAdmin(admin.ModelAdmin):
    fields = ['name', ]
    list_display = ('name',)
    inlines = [
        DatasetOptionsInlineAdmin,
    ]

@admin.register(AxisOptionsGroupModel)
class AxisOptionsAdmin(admin.ModelAdmin):
    fields = ['name', ]
    list_display = ('name',)
    inlines = [
        AxisOptionsInlineAdmin,
    ]

# Register Axes
# ------------------------
@admin.register(AxisModel)
class AxisAdmin(admin.ModelAdmin):
    fields = ['label', 'slug', 'type', 'display', 'weight', 'options']
    readonly_fields = ['slug']
    list_display = ('label',)
