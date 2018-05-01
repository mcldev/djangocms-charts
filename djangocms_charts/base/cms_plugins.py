from cms.plugin_base import CMSPluginBase
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class ChartsBasePlugin(CMSPluginBase):

    text_enabled = True
    readonly_fields = ('chart_id', 'chart_container_id', 'chart_title_id', 'legend_id')
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Headers'), {
            'fields': (('labels_top', 'labels_left', 'data_series_format'),)
        }),
        (_("Input Table or CSV"), {
            'fields': ('table_data', 'csv_upload')
        }),
        (_("Legend Settings"), {
            'fields': (('title_display', 'legend_display', 'legend_position'))
        }),
        (_("Chart Settings"), {
            'fields': (('chart_width', 'chart_height', 'chart_position'))
        }),
        (_("Chart Classes"), {
            'classes': ('collapse',),
            'fields': ('chart_container_classes', 'chart_title_classes', 'chart_classes', 'legend_classes')
        }),
        (_("Chart Object Ids"), {
            'classes': ('collapse',),
            'fields': ('chart_container_id', 'chart_title_id', 'chart_id', 'legend_id')
        }),
    )

    def get_data(self, instance):
        raise NotImplementedError(  # pragma: no cover
                'Get data function must be created to pass to chart')

    # def get_additional_context(self, context, instance, placeholder):
    #     return context

    def render(self, context, instance, placeholder):
        data = None
        error=None
        # Get data in correct format for javascript chart
        try:
            data = self.get_data(instance)
        except Exception as err:
            error = str(err)

        context.update({
            'name': instance.name,
            'data': data,
            'error': error,
            'instance': instance
        })
        # Add extra context (e.g. global_settings) as required by chart type
        if callable(self.get_additional_context):
            self.get_additional_context(context, instance, placeholder)

        return context

    # Required if this plugin is within a parent text plugin - inoperable otherwise.
    # http://www.megaicons.net/iconspack-624/21477/
    def icon_src(self, instance):
        return settings.STATIC_URL + "djangocms_charts/img/chart-icon.png"

    def response_change(self, request, obj):
        response = super(ChartsBasePlugin, self).response_change(request, obj)
        if 'csv_upload' in request.FILES.keys():
            self.object_successfully_changed = False
        return response

    class Meta:
        abstract = True
