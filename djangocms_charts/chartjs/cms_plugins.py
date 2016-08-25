from django.utils.translation import ugettext_lazy as _
import json
from djangocms_charts.base.cms_plugins import ChartsBasePlugin
from djangocms_charts.utils import *
from .views.chart_views import ChartJsView
from .forms import ChartJsInputForm
from .models import *
from .models_global import get_current_chartjs_global_settings


class ChartJsBasePlugin(ChartsBasePlugin):

    module = _("ChartJs")
    render_template = "djangocms_charts/chartjs/chartjs.html"

    # Init requires same inputs as parent-parent
    def __init__(self, *args, **kwargs):
        super(ChartJsBasePlugin, self).__init__(*args, **kwargs)
        self.get_option_fieldsets()
        self.load_form()

    def load_form(self):
        ChartJsInputForm.chart_type=self.model.chart_type
        self.form = ChartJsInputForm

    def get_chart_options(self, instance):
        filter_fields_lambda = lambda f : f.startswith('option_')
        convert_fields_lambda = lambda f : str(f).replace('option_','')
        convert_values_lambda = lambda v : str(v).replace("\"", "'") if isinstance(v, basestring) else v
        chart_options = get_fields_and_values_from_instance(instance, filter_fields_lambda= filter_fields_lambda, convert_fields_lambda=convert_fields_lambda, convert_values_lambda =convert_values_lambda )
        return chart_options

    def get_data(self, instance):
        chartjs_data_view = ChartJsView(instance)
        data = chartjs_data_view.get_json()
        return data

    def get_additional_context(self, context, instance, placeholder):
        context.update({
            'global_settings': get_current_chartjs_global_settings(),
            'chart_options': self.get_chart_options(instance),
        })
        return context

    # fieldsets = ChartsBasePlugin.fieldsets
    def get_option_fieldsets(self):
        # Get parent fieldsets
        options_query = lambda f: f.startswith('option_')
        option_fieldsets = get_fields_from_obj(self.model, options_query)
        if option_fieldsets:
            self.fieldsets += (
                (_("Advanced Chart Options"), {
                    'classes': ('collapse',),
                    'fields': option_fieldsets
                }),
            )

    class Meta:
        abstract = True


class ChartJsLinePlugin(ChartJsBasePlugin):
    model = ChartJsLineModel
    name = _('Line Chart')


class ChartJsBarPlugin(ChartJsBasePlugin):
    model = ChartJsBarModel
    name = _('Bar Chart')


class ChartJsRadarPlugin(ChartJsBasePlugin):
    model = ChartJsRadarModel
    name = _('Radar Chart')


class ChartJsPolarPlugin(ChartJsBasePlugin):
    model = ChartJsPolarModel
    name = _('Polar Area Chart')


class ChartJsPiePlugin(ChartJsBasePlugin):
    model = ChartJsPieModel
    name = _('Pie Chart')


class ChartJsDoughnutPlugin(ChartJsBasePlugin):
    model = ChartJsDoughnutModel
    name = _('Doughnut Chart')