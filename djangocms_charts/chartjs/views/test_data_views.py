
"""Tools to build Line charts parameters."""
from .chart_views import ChartJsView
from djangocms_charts.chartjs.consts import *

# Replace labels and data with sample data
class Test_Dataset_Instance(object):
    chart_type = None
    data_series_format = 'rows'
    labels_top = True
    labels_left = True
    table_data = [["", "January", "February", "March", "April", "May", "June", "July"],
                    ['Series 1', 75, 44, 92, 11, 44, 95, 35],
                    ['Series 2', 41, 92, 18, 3, 73, 87, 92],
                    ['Series 3', 87, 21, 94, 3, 90, 13, 65]]


class Test_DataArray_Instance(object):
    chart_type = None
    data_series_format = 'cols'
    labels_top = True
    labels_left = False
    table_data = [["January", "February", "March", "April", "May", "June", "July"],
                    [75, 44, 92, 11, 44, 95, 35]]



# Get Main instance of Chart Data
dataset_instance = Test_Dataset_Instance()
data_array_instance = Test_DataArray_Instance()

#Line Chart Test
def chartjs_line_json_view(request):
    dataset_instance.chart_type = CHART_TYPES.LINE
    return ChartJsView(dataset_instance).get_json_view()

#Bar Chart Test
def chartjs_bar_json_view(request) :
    dataset_instance.chart_type = CHART_TYPES.BAR
    return ChartJsView(dataset_instance).get_json_view()

#Radar Chart Test
def chartjs_radar_json_view(request):
    dataset_instance.chart_type = CHART_TYPES.RADAR
    return ChartJsView(dataset_instance).get_json_view()

#Polar Chart Test
def chartjs_polar_json_view(request):
    data_array_instance.chart_type = CHART_TYPES.POLAR
    return ChartJsView(data_array_instance).get_json_view()

#Pie Chart Test
def chartjs_pie_json_view(request) :
    data_array_instance.chart_type = CHART_TYPES.PIE
    return ChartJsView(data_array_instance).get_json_view()

#Doughnut Chart Test
def chartjs_doughnut_json_view(request) :
    data_array_instance.chart_type = CHART_TYPES.DOUGHNUT
    return ChartJsView(data_array_instance).get_json_view()


