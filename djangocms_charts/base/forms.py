import csv
import io

from django import forms
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _

from djangocms_charts.widgets import *
from djangocms_charts.utils import *
from .consts import *

class ChartsBaseInputForm(ModelForm):

    # Chart Type - static value assigned on each child
    chart_type = None

    def __init__(self, *args, **kwargs):
        super(ChartsBaseInputForm, self).__init__(*args, **kwargs)
        InputTableWidget.chart_type = self.chart_type

    # Table input / csv upload
    table_data = forms.CharField(widget=InputTableWidget)
    csv_upload = forms.FileField(label=_("upload .csv file"), help_text=_("Upload a .csv file to populate the table."), required=False)

    # Legend Position
    legend_position = forms.ChoiceField(required=False, widget=forms.Select, choices=LEGEND_POSITIONS.get_choices)

    # Chart Position
    chart_position = forms.ChoiceField(required=False, widget=forms.Select, choices=CHART_POSITIONS.get_choices)

    #Data series in Rows/Cols
    data_series_format = forms.ChoiceField(label=_('Data series in Rows or Columns:'), required=False, widget=forms.Select, choices=(('rows', 'Rows'),('cols', 'Cols')))

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

    class Meta:
        abstract = True
