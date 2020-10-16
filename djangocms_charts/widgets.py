import json

from django.conf import settings
from django.forms import Textarea
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation.trans_real import get_language

from .consts import CHART_TYPES


class InputTableWidget(Textarea):

    class Media:
        js = (
                'djangocms_charts/input/js/handsontable.full.js',
                'djangocms_charts/input/js/jquery.contextMenu.js',
                'djangocms_charts/input/js/jquery-ui.position.js',
                'djangocms_charts/input/js/json2.js',
                'djangocms_charts/input/js/bootstrap3-typeahead.js',
            )
        css = {
            'all': (
                'djangocms_charts/input/css/handsontable.full.modified.css',
                'djangocms_charts/input/css/jquery.contextMenu.css',
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
            'STATIC_URL': settings.STATIC_URL,
        }
        return mark_safe(render_to_string('djangocms_charts/widgets/input-table.html', context))

    def render(self, name, value, attrs=None, **kwargs):
        return self.render_textarea(name, value, attrs) + \
            self.render_additions(name, value, attrs)

