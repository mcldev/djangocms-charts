from cms.plugin_pool import plugin_pool

from .chartjs.cms_plugins import *

plugin_pool.register_plugin(ChartJsLinePlugin)
plugin_pool.register_plugin(ChartJsBarPlugin)
plugin_pool.register_plugin(ChartJsRadarPlugin)
plugin_pool.register_plugin(ChartJsPolarPlugin)
plugin_pool.register_plugin(ChartJsPiePlugin)
plugin_pool.register_plugin(ChartJsDoughnutPlugin)