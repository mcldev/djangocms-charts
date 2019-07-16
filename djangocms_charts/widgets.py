import json

from django.conf import settings
from django.forms import Textarea
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation.trans_real import get_language

from djangocms_charts.chartjs.consts import CHART_TYPES


class InputTableWidget(Textarea):

    chart_type = None

    class Media:
        js = (
                'djangocms_charts/ext-input/js/handsontable.full.js',
                'djangocms_charts/ext-input/js/jquery.contextMenu.js',
                'djangocms_charts/ext-input/js/jquery-ui.position.js',
                'djangocms_charts/ext-input/js/json2.js',
                'djangocms_charts/ext-input/js/bootstrap3-typeahead.js',
            )
        css = {
            'all': (
                'djangocms_charts/ext-input/css/handsontable.full.modified.css',
                'djangocms_charts/ext-input/css/jquery.contextMenu.css',
                ),
        }

    def render_textarea(self, name, value, attrs=None):
        return super(InputTableWidget, self).render(name, value, attrs)

    def render_additions(self, name, value, attrs=None):
        language = get_language().split('-')[0]
        context = {
            'name': name,
            'language': language,
            'data': value,
            'chart_type': self.chart_type,
            'STATIC_URL': settings.STATIC_URL,
            'LABEL_VALUE_CHART_TYPES': json.dumps(CHART_TYPES.get_label_value_types)
        }
        return mark_safe(render_to_string('djangocms_charts/widgets/input-table.html', context))

    def render(self, name, value, attrs=None, **kwargs):
        return self.render_textarea(name, value, attrs) + \
            self.render_additions(name, value, attrs)

