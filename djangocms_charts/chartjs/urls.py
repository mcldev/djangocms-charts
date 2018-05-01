from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import include, url

urlpatterns = [

       # ChartJS JSON TEST Data Views
       # --------------------------------
       # Line chart
       url(r'^json/line-test/$', include('djangocms_charts.chartjs.views.test_data_views.chartjs_line_json_view'), name='chartjs_line_json_test'),
       # Bar chart
       url(r'^json/bar-test/$', include('djangocms_charts.chartjs.views.test_data_views.chartjs_bar_json_view'), name='chartjs_bar_json_test'),
       # Radar chart
       url(r'^json/radar-test/$', include('djangocms_charts.chartjs.views.test_data_views.chartjs_radar_json_view'), name='chartjs_radar_json_test'),
       # Polar Area chart
       url(r'^json/polar-test/$', include('djangocms_charts.chartjs.views.test_data_views.chartjs_polar_json_view'), name='chartjs_polar_json_test'),
       # Pie chart
       url(r'^json/pie-test/$', include('djangocms_charts.chartjs.views.test_data_views.chartjs_pie_json_view'), name='chartjs_pie_json_test'),
       # Doughnut chart
       url(r'^json/doughnut-test/$', include('djangocms_charts.chartjs.views.test_data_views.chartjs_doughnut_json_view'), name='chartjsdoughnut_json_test'),

       # ChartJS JSON Data Views
       # --------------------------------
       # Direct query to charts json values [chartjsmodel_id]
       url(r'^json/(?P<chartjsmodel_id>[0-9]+)/$', include('djangocms_charts.chartjs.views.data_views.get_chartjs_json'), name='chartjs_json'),

]
