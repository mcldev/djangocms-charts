
"""Tools to build Line charts parameters."""
from django.shortcuts import get_object_or_404
from .chart_views import ChartJsView
from djangocms_charts.chartjs.models import ChartJsBaseModel

def get_chartjs_json(request, chartjsmodel_id):
    #Get Chart Data
    chart_data = get_object_or_404(ChartJsBaseModel, pk=chartjsmodel_id)
    chart_view = ChartJsView(chart_data)
    return chart_view.get_json_view()
