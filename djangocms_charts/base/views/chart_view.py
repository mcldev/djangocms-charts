from .json_view import JSONView
import json
from djangocms_charts.utils import *
from six import string_types

class BaseChartView(JSONView):

    # Chart type to be defined when calling the base class
    chart_type = None
    data = None
    labels_top = None
    labels_left = None
    data_series_in_rows = None

    def get_chart_type(self):
        if self.chart_type == None:
            raise NotImplementedError(  # pragma: no cover
                'Chart type is not set, use class CHART_TYPE.LINE, ...BAR etc.')
        else:
            return self.chart_type

    # Main function to return JSON data - overwriting ContextMixin
    def __init__(self, chart_data_instance, **kwargs):

        super(BaseChartView, self).__init__(**kwargs)

        self.chart_type = chart_data_instance.chart_type
        self.data_series_in_rows = (chart_data_instance.data_series_format == 'rows')

        #If Table data is a string (as saved by django) then load it as array.
        table_data = json.loads(chart_data_instance.table_data) if isinstance(chart_data_instance.table_data, string_types) else chart_data_instance.table_data

        # Switch top/left if data is transposed
        if self.data_series_in_rows:
            self.labels_top = chart_data_instance.labels_top
            self.labels_left = chart_data_instance.labels_left
            self.data = table_data
        else :
            self.labels_top = chart_data_instance.labels_left
            self.labels_left = chart_data_instance.labels_top
            self.data = transpose(table_data)

    # Set the data start for rows
    def _row_start(self):
        row_start = 0
        if(self.labels_top) :
            row_start = 1
        return row_start

    # Set the data start for cols
    def _col_start(self):
        col_start = 0
        if(self.labels_left) :
            col_start = 1
        return col_start

    # Get the data excluding labels on top/left if set - convert all values to float!~
    def get_data(self):
        get_data = [map(float, self.data[i][self._col_start():]) for i in range(self._row_start(), len(self.data))]
        return get_data

    # Data is already transposed so Labels are always at the top
    def get_labels(self):
        # For columns of data with top row = x-axis label
        if(self.labels_top) :
            return self.data[0][self._col_start():]

        # For no data x-axis labels
        return None

    # Data is already transposed so Data Series Labels are always at the left
    def get_series_labels(self):
        # For rows of data with first col = series label
        if(self.labels_left) :
            return [self.data[i][0] for i in range(self._row_start(), len(self.data))]

        # For no data series labels
        return None

    #Chart Options to be specified for each instance
    def get_context_data(self):
        raise NotImplementedError(  # pragma: no cover
            'You should return context data - in the required format')

    #Chart Options to be specified for each instance
    def get_chart_options(self):
        raise NotImplementedError(  # pragma: no cover
            'You should return the options for this chart - in the required format')

    # Return the JSON string
    def get_json(self):
        return self.convert_context_to_json(self.get_context_data())

    #Return an HTTP view of the JSON data
    def get_json_view(self):
        return self.render_to_response(self.get_context_data())

    class Meta:
        abstract = True