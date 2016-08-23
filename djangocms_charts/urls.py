
from __future__ import absolute_import, print_function, unicode_literals
from django.conf.urls import *  # NOQA

# Not used... need parent url (e.g. 'chartjs/') in app.urls

urlpatterns = patterns('',
                       (r'^chartjs/', include('djangocms_charts.chartjs.urls')),
                       (r'^highcharts/', include('djangocms_charts.highcharts.urls'))
                       )


