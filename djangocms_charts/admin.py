from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin

from .forms import GlobalOptionsInlineForm, ChartOptionsInlineForm, DatasetOptionsInlineForm, AxisOptionsInlineForm, \
    ColorInputForm
from .models import GlobalOptionsGroupModel, GlobalOptionsModel, \
    ChartOptionsGroupModel, ChartOptionsModel, \
    DatasetOptionsGroupModel, DatasetOptionsModel, \
    AxisOptionsGroupModel, AxisOptionsModel, ChartSpecificOptionsModel, DatasetSpecificOptionsModel
from .models_colors import ColorModel, ColorGroupModel


# ------------------------

# Inline Forms for Options

# ------------------------

class OptionsInlineBase(admin.TabularInline):
    fields = ['label', 'type', 'value']
    list_display = ('label', 'type', 'value')
    extra = 0

# Options Groups Inlines
# ------------------------
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

# Specific Options inlines
# ------------------------
class ChartSpecificOptionsInlineAdmin(OptionsInlineBase):
    model = ChartSpecificOptionsModel
    form = ChartOptionsInlineForm

class DatasetSpecificOptionsInlineAdmin(OptionsInlineBase):
    model = DatasetSpecificOptionsModel
    form = DatasetOptionsInlineForm


# Register Options Groups
# ------------------------
@admin.register(GlobalOptionsGroupModel)
class GlobalOptionsAdmin(admin.ModelAdmin):
    fields = ['name', 'enabled', 'site', 'colors']
    list_display = ('name', 'enabled')
    inlines = [
        GlobalOptionsInlineAdmin,
    ]

@admin.register(ChartOptionsGroupModel)
class ChartsOptionsAdmin(admin.ModelAdmin):
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
    fields = ['name', 'slug', 'type', 'display', 'weight']
    readonly_fields = ['slug']
    list_display = ('name', 'type')
    inlines = [
        AxisOptionsInlineAdmin,
    ]

# Register Colour Admins
# ------------------------
class ColorsInline(admin.TabularInline):
    fields = ['types', 'labels', 'colors']
    list_display = ['types', 'labels', 'colors']
    extra = 0
    model = ColorModel
    form = ColorInputForm


@admin.register(ColorGroupModel)
class ColorGroupAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name',)
    inlines = [
        ColorsInline,
    ]
