from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import include, url
from djangocms_charts.chartjs.views.test_data_views import *
from djangocms_charts.chartjs.views.data_views import get_chartjs_json

urlpatterns = [

       # ChartJS JSON TEST Data Views
       # --------------------------------
       # Line chart
       url(r'^json/line-test/$', chartjs_line_json_view, name='chartjs_line_json_test'),
       # Bar chart
       url(r'^json/bar-test/$', chartjs_bar_json_view, name='chartjs_bar_json_test'),
       # Radar chart
       url(r'^json/radar-test/$', chartjs_radar_json_view, name='chartjs_radar_json_test'),
       # Polar Area chart
       url(r'^json/polar-test/$', chartjs_polar_json_view, name='chartjs_polar_json_test'),
       # Pie chart
       url(r'^json/pie-test/$', chartjs_pie_json_view, name='chartjs_pie_json_test'),
       # Doughnut chart
       url(r'^json/doughnut-test/$', chartjs_doughnut_json_view, name='chartjsdoughnut_json_test'),

       # ChartJS JSON Data Views
       # --------------------------------
       # Direct query to charts json values [chartjsmodel_id]
       url(r'^json/(?P<chartjsmodel_id>[0-9]+)/$', get_chartjs_json, name='chartjs_json'),

]
