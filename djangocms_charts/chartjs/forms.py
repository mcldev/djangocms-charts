from django import forms
from .consts import *
from .models import *
from djangocms_charts.base.forms import ChartsBaseInputForm
from djangocms_charts.widgets import *

class ChartJsInputForm(ChartsBaseInputForm):

    # Clean form and validate dependent fields
    def clean(self):
        cleaned_data = super(ChartJsInputForm, self).clean()

        # Check if either label has been selected
        top = cleaned_data['labels_top']
        left = cleaned_data['labels_left']
        data_series_in_rows = cleaned_data['data_series_format'] == 'rows'

        msg = "Data Labels are required (for x-axis)"

        if self.chart_type in CHART_TYPES.get_label_value_types :
            if not left and data_series_in_rows:
                self.add_error('labels_left', msg)
        else :
            if not top and data_series_in_rows :
                self.add_error('labels_top', msg)
            elif not left and not data_series_in_rows :
                self.add_error('labels_left', msg)


    class Meta:
        model = ChartJsBaseModel
        exclude = (
            'page',
            'position',
            'placeholder',
            'language',
            'plugin_type',
        )