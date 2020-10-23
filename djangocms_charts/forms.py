import csv
import io
import json
from django_select2.forms import Select2Widget
from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _

from djangocms_charts.consts import get_chartjs_global_options, OPTION_DATA_TYPES, get_chartjs_dataset_options, \
    get_chartjs_chart_options, get_chartjs_axis_options, CHART_TYPES, COLOR_LABELS
from djangocms_charts.widgets import *
from djangocms_charts.utils import *


class OptionsInlineFormBase(ModelForm):
    type = forms.CharField(required=True,  widget=forms.Select(choices=OPTION_DATA_TYPES))
    value = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))

    def clean(self):
        cleaned_data = super().clean()
        val = cleaned_data.get('value')
        val_type = cleaned_data.get('type')
        try:
            check_val = self.instance.get_json_value(val, val_type)
        except Exception as err:
            raise ValidationError(
                _('Invalid value: %(value)s'),
                code='invalid',
                params={'value': val},
            )

    class Media:
        js = (
            'djangocms_charts/input/js/jquery-3.5.1.min.js',
            'djangocms_charts/input/custom/admin_fixes.js',
        )

        css = {
            'all': (
                'djangocms_charts/input/custom/admin_styles.css',
            )
        }

# Option Forms with different inputs:

class GlobalOptionsInlineForm(OptionsInlineFormBase):
    label = forms.CharField(required=True, widget=Select2Widget(choices=get_chartjs_global_options()))


class ChartOptionsInlineForm(OptionsInlineFormBase):
    label = forms.CharField(required=True, widget=Select2Widget(choices=get_chartjs_chart_options()))


class DatasetOptionsInlineForm(OptionsInlineFormBase):
    label = forms.CharField(required=True, widget=Select2Widget(choices=get_chartjs_dataset_options()))


class AxisOptionsInlineForm(OptionsInlineFormBase):
    label = forms.CharField(required=True, widget=Select2Widget(choices=get_chartjs_axis_options()))


# Dataset form

class DatasetInputForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(DatasetInputForm, self).__init__(*args, **kwargs)

    caption = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))

    # Table input / csv upload
    table_data = forms.CharField(widget=InputTableWidget)
    csv_upload = forms.FileField(label=_("upload .csv file"), help_text=_("Upload a .csv file to populate the table."), required=False)

    # Add the cleaned csv data to the table
    def clean_table_data(self):
        if self.cleaned_data['table_data']:
            table_data = json.loads(self.cleaned_data['table_data'])

            # Check for empty rows
            data_check_rows = []
            for row in table_data:
                row_check = False
                for cell in row:
                    if cell:
                        row_check = True
                        break
                if row_check :
                    data_check_rows.append(row)

            # Check for empty cols
            data_check_cols=[]
            data_check_rows = transpose(data_check_rows)
            for col in data_check_rows:
                col_check = False
                for cell in col:
                    if cell:
                        col_check = True
                        break
                if col_check :
                    data_check_cols.append(col)
            data_check_cols = transpose(data_check_cols)

            return json.dumps(list(data_check_cols))


    # Add the cleaned csv data to the table
    def clean_csv_upload(self):
        if self.cleaned_data['csv_upload']:
            encoding = self.cleaned_data['csv_upload'].charset if self.cleaned_data['csv_upload'].charset else 'utf-8-sig'
            f = io.TextIOWrapper(self.cleaned_data['csv_upload'].file, encoding=encoding)
            csv_reader = csv.reader(f, dialect='excel')
            data = []
            for row in csv_reader:
                data.append(row)
            self.cleaned_data['table_data'] = json.dumps(data)
            self.csv_uploaded = True


    def clean(self):
        cleaned_data = super().clean()
        table_data = cleaned_data.get("table_data")
        check_data = json.loads(table_data)
        if not check_data:
            raise ValidationError("Error: missing chart data from table or CSV file input")

    class Meta:
        labels = {
            'dataset_options_group': _('Dataset options'),
        }



# Color Inline input form
# ------------------------

class ColorInputForm(ModelForm):
    types = forms.MultipleChoiceField(label=_('Select Chart Types'), help_text=_('Hold CTRL for multiple values'),
                                      choices=CHART_TYPES.get_choices)
    labels = forms.MultipleChoiceField(label=_('Select Namespace Labels'), help_text=_('Hold CTRL for multiple values'),
                                       choices=COLOR_LABELS)
    colors = forms.CharField(label=_('Select Colors for each dataset'), widget=MultiColorSelectWidget,
                             help_text=_('Click and drag changes to change order, or enter manually'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial and self.initial['types']:
            self.initial['types'] = json.loads(self.initial['types'].replace("'", '"'))
        if self.initial and self.initial['labels']:
            self.initial['labels'] = json.loads(self.initial['labels'].replace("'", '"'))

