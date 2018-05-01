
from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import include, url

# Not used... need parent url (e.g. 'chartjs/') in app.urls

urlpatterns = [
    url(r'^chartjs/', include('djangocms_charts.chartjs.urls')),
    url(r'^highcharts/', include('djangocms_charts.highcharts.urls')),
]


