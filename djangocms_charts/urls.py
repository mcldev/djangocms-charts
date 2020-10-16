from django.urls import path
from djangocms_charts.views import get_chart_as_json, get_global_options_as_json


app_name = 'djangocms_charts'


urlpatterns = [
    path('get_chart_as_json/<int:chart_id>/', get_chart_as_json, name="get_chart_as_json"),
    path('get_global_options_as_json/<int:options_id>/', get_global_options_as_json, name="get_global_options_as_json"),
]


