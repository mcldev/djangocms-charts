from cms.models import CMSPlugin
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from .models_datasets import DatasetBase
from .models_options import *
from .models_axes import AxisModel

import djangocms_charts.cache as charts_cache

# --------------------------------------

# Main Chart Model

# --------------------------------------
class ChartModel(DatasetBase, CMSPlugin):
    """
    Charts Model
    """
    #     options: {
    #         title: {
    #             display: true,
    #             text: 'Custom Chart Title'
    #         }
    #     }

    caption = models.TextField(_('Caption text below chart'), null=True, blank=True)

    # Chart Custom Settings
    display_title = models.BooleanField(_("Display Title"), default=True)
    chart_width = models.CharField(_("Chart Width"), max_length=50, null=True, blank=True)
    chart_height = models.CharField(_("Chart Height"), max_length=50, null=True, blank=True)

    # Classes for each chart object
    chart_container_classes = models.TextField(_("Additional classes for Chart Container"), blank=True)
    chart_classes = models.TextField(_("Additional classes for Chart"), blank=True)

    # Chart options
    chart_options = models.ForeignKey(ChartOptionsGroupModel, on_delete=models.CASCADE,
                                      related_name="chart_options", blank=True, null=True)

    def get_chart_width(self):
        if self.chart_width.isnumeric():
            return f'{self.chart_width}px'
        else:
            return self.chart_width
        
    def get_chart_height(self):
        if self.chart_height.isnumeric():
            return f'{self.chart_height}px'
        else:
            return self.chart_height
        
    def get_chart_as_dict(self):

        # Get Cached
        # -------------------
        cached_chart_dict = charts_cache.get(self.__class__.__name__, self.id)
        if cached_chart_dict:
            return cached_chart_dict

        # Get Child Datasets
        # -------------------
        child_datasets = self.child_plugin_instances or []

        # Get all Source data
        # -------------------
        datasets, x_labels, x_axes, y_axes = self.get_as_dict()

        # Get Chart Options
        # -------------------
        chart_options = None
        if self.chart_options:
            chart_options = self.chart_options.get_as_dict().get('options', None)

        # Append Child datasets
        # -------------------
        for other_dataset in child_datasets:
            _datasets, _x_labels, _x_axes, _y_axes = other_dataset.get_as_dict()
            datasets = _datasets + datasets
            if not any(x_labels):
                x_labels = _x_labels
            x_axes += _x_axes
            y_axes += _y_axes

        # Add common data to final Dictionary
        # -----------------------------------
        chart_dict = {}
        chart_dict['type'] = self.chart_type

        # Append Datasets
        chart_dict['data'] = {'datasets': datasets}

        # Get X Labels
        # -------------------
        if any(x_labels):
            chart_dict['data']['labels'] = x_labels

        # Get Options Dictionary
        # -------------------
        options_dict = chart_dict.setdefault('options', {})

        # Append Axes
        # -------------------
        if any(x_axes) or any(y_axes):
            axis_dict = options_dict.setdefault('scales', {})
            if x_axes:
                axis_dict['xAxes'] = x_axes
            if y_axes:
                axis_dict['yAxes'] = y_axes

        # Add Title
        # -------------------
        if self.label:
            title_dict = {
                'title': {
                    'display': self.display_title,
                    'text': self.label,
                }
            }
            options_dict.update(title_dict)

        # Add/override custom options
        # -------------------
        if chart_options:
            options_dict.update(chart_options)

        # Set Cache
        # -------------------
        charts_cache.set(self.__class__.__name__, self.id, chart_dict)

        return chart_dict


    # Chart name
    @property
    def chart_name(self):
        get_name = str(f'{self.type}_{self.label or self.id}')
        #  Replace all non-chars
        get_name = slugify(get_name)
        return get_name

    # Chart Id
    def chart_id(self):
        return f'chart_{self.id}'

    # Chart Container Id
    def chart_container_id(self):
        return f'chart-container_{self.id}'

    # Chart Name
    def __str__(self):
        return self.chart_name

    search_fields = ('name', 'table_data')


# --------------------------------------

# Dataset Model

# --------------------------------------
class DatasetModel(CMSPlugin, DatasetBase):
    """
    Charts Model
    """
    # Dataset name
    @property
    def dataset_name(self):
        get_name = str(f'{self.type}_{self.label or self.id}')
        #  Replace all non-chars
        get_name = slugify(get_name)
        return get_name

    # Dataset Id
    @property
    def dataset_id(self):
        return f'dataset_{self.id}'

    # Dataset Name
    def __str__(self):
        return self.dataset_name

    search_fields = ('name', 'table_data')

