import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
import consts

def get_chart_class():
    return ChartsBaseModel.get_class_string()

class ChartsBaseModel(CMSPlugin):
    """
    Charts Model
    """
    name = models.CharField(_("Name"), max_length=256)
    chart_type = None

    # Table data
    table_data = models.TextField(_("Chart Table data"), blank=True)

    # Set Headers in Top and/or Left
    labels_top = models.BooleanField(_("Labels top row"), default=True, help_text="here is some help")
    labels_left = models.BooleanField(_("Labels left column"), default=True)
    data_series_format = models.CharField(_("Data series in Rows or Cols)"), max_length=10, default='rows')

    # Chart Parameters
    chart_width = models.IntegerField(_("Chart Width"), default=400)
    chart_height = models.IntegerField(_("Chart Height"), default=400)
    chart_position = models.CharField(_("Chart Position"), max_length=100, blank=True)

    # Legend
    title_display = models.BooleanField(_("Display Title"), default=True)
    legend_display = models.BooleanField(_("Display Legend"), default=True)
    legend_position = models.CharField(_("Legend Position"), max_length=100, blank=True)

    # Get chart class - defined by cls.chart_type e.g. line-chart
    @classmethod
    def get_class_string(cls):
        chart_type = cls.chart_type.lower() if cls.chart_type else ''
        return str('{0}-chart ').format(chart_type)

    # Classes for each chart object
    chart_container_classes = models.TextField(_("Additional classes for Chart Container"), blank=True, default=get_chart_class)
    chart_title_classes = models.TextField(_("Additional classes for Chart Title"), blank=True, default=get_chart_class)
    chart_classes = models.TextField(_("Additional classes for Chart"), blank=True, default=get_chart_class)
    legend_classes = models.TextField(_("Additional classes for Legend"), blank=True, default=get_chart_class)

    # Chart name
    def _chart_name(self):
        get_name = str("{0}_{1}").format(self.name,self.id).lower() # get name_id
        #  Replace all non-chars
        get_name = re.sub(r"[^\w\s]", '', get_name)
        # Replace all spaces with _
        get_name = re.sub(r"\s+", '_', get_name)
        return get_name

    # Chart Id
    def chart_id(self):
        get_chart_id = self.chart_type.lower() + '-chart_' + self._chart_name()
        return get_chart_id
    chart_id.short_description = 'Chart Id'

    # Chart Container Id
    def chart_container_id(self):
        return self.chart_type.lower() + '-chart-container_' + self._chart_name()
    chart_container_id.short_description = 'Chart Container Id'

    # Chart Title Id
    def chart_title_id(self):
        return self.chart_type.lower() + '-chart-title_' + self._chart_name()
    chart_title_id.short_description = 'Chart Title Id'

    # Legend Id
    def legend_id(self):
        return self.chart_type.lower() + '-chart-legend_' + self._chart_name()
    legend_id.short_description = 'Legend Id'

    def set_legend_width(self):
        return self.legend_position_in_top_bottom()

    def legend_position_in_top_bottom(self):
        top_bottom_positions = [consts.LEGEND_POSITIONS.BOTTOM, consts.LEGEND_POSITIONS.TOP]
        top_bottom_labels = [consts.get_legend_class(pos) for pos in top_bottom_positions]
        return self.legend_position in top_bottom_labels


    # Chart Name
    def __unicode__(self):
        return self.name

    search_fields = ('name', 'table_data')

    class Meta:
        abstract = True


