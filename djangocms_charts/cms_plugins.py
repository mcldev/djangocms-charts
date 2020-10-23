import json

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from djangocms_charts.admin import ChartSpecificOptionsInlineAdmin, DatasetSpecificOptionsInlineAdmin
from djangocms_charts.forms import DatasetInputForm
from djangocms_charts.models import ChartModel, DatasetModel, GlobalOptionsGroupModel



@plugin_pool.register_plugin
class ChartJsPlugin(CMSPluginBase):

    module = _("Charts")
    name = 'ChartJS Plugin'
    render_template = "djangocms_charts/chartjs.html"
    model = ChartModel
    allow_children = True
    child_classes = ['DatasetPlugin']
    form = DatasetInputForm
    inlines = [
        ChartSpecificOptionsInlineAdmin,
    ]
    fieldsets = (
        (None, {
            'fields': ('label', 'type', 'caption')
        }),
        (_('Data Format'), {
            'fields': (('labels_top', 'labels_left'), 'data_series_format')
        }),
        (_("Input Table or CSV"), {
            'fields': ('table_data', 'csv_upload')
        }),
        (_("Dataset Colors"), {
            'fields': ('color_by_dataset', 'colors')
        }),
        (_("Chart Options"), {
            'fields': ('chart_options_group', 'dataset_options_group', 'xAxis', 'yAxis')
        }),
        (_("Chart Settings"), {
            'fields': ('display_title', 'display_legend', 'legend_position')
        }),
        (_("Advanced Settings and Classes"), {
            'classes': ('collapse',),
            'fields': ('chart_width', 'chart_height', 'chart_container_classes', 'chart_classes',)
        }),
    )

    def render(self, context, instance, placeholder):
        context = super(ChartJsPlugin, self).render(context, instance, placeholder)
        global_options_list = GlobalOptionsGroupModel.get_global_options()
        chart_data = instance.get_chart_as_dict()
        chart_json = json.dumps(chart_data)
        color_by_dataset = instance.color_by_dataset if instance.color_by_dataset is not None else False
        color_by_dataset = json.dumps(color_by_dataset)
        enable_chartjs_sass = getattr(settings, 'DJANGOCMS_CHARTS_ENABLE_CHARTJS_SASS', True)

        context.update({
            'chart_data': chart_json,
            'global_options': global_options_list,
            'color_by_dataset': color_by_dataset,
            'enable_chartjs_sass': enable_chartjs_sass,
        })
        return context


@plugin_pool.register_plugin
class DatasetPlugin(CMSPluginBase):
    render_plugin = False
    name = 'ChartJS Dataset'
    model = DatasetModel
    require_parent = True
    parent_classes = ['ChartJsPlugin']
    form = DatasetInputForm
    inlines = [
        DatasetSpecificOptionsInlineAdmin,
    ]
    fieldsets = (
        (None, {
            'fields': ('label', 'type')
        }),
        (_('Data Format'), {
            'fields': (('labels_top', 'labels_left',), 'data_series_format')
        }),
        (_("Input Table or CSV"), {
            'fields': ('table_data', 'csv_upload')
        }),
        (_("Dataset Colors"), {
            'fields': ('color_by_dataset', 'colors')
        }),
        (_("Datasetl Options"), {
            'fields': ('dataset_options_group', 'xAxis', 'yAxis')
        }),
    )

