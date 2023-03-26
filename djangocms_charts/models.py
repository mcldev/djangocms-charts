from cms.models import CMSPlugin

from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

import djangocms_charts.cache as charts_cache
from djangocms_charts.utils import get_unique_list
from .consts import LEGEND_POSITIONS

from .models_axes import AxisOptionsGroupModel, AxisOptionsModel
from .models_colors import ColorGroupModel, ColorModel
from .models_datasets import DatasetBase
from .models_options import *


# --------------------------------------

# Main Chart Model

# --------------------------------------

class ChartModel(CMSPlugin, DatasetBase):
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

    # Chart Common Settings
    display_title = models.BooleanField(_("Display Title"), default=True)
    display_legend = models.BooleanField(_("Display Legend"), default=True)
    legend_position = models.CharField(_("Legend Position"), max_length=100, blank=True, null=True,
                                       choices=LEGEND_POSITIONS, default=LEGEND_POSITIONS[0][0])

    # Custom Classes and Settings for each chart
    chart_width = models.CharField(_("Chart Width"), max_length=50, null=True, blank=True)
    chart_height = models.CharField(_("Chart Height"), max_length=50, null=True, blank=True)
    chart_container_classes = models.TextField(_("Additional classes for Chart Container"), blank=True)
    chart_classes = models.TextField(_("Additional classes for Chart"), blank=True)

    # Chart options
    chart_options_group = models.ForeignKey(ChartOptionsGroupModel, on_delete=models.CASCADE,
                                            related_name="chart_options", blank=True, null=True)

    def copy_relations(self, old_instance):
        # Before copying related objects from the old instance, the ones
        # on the current one need to be deleted. Otherwise, duplicates may
        # appear on the public version of the page
        self.options.all().delete()

        for option in old_instance.options.all():
            # standard Django way of copying a saved model instance
            option.pk = None
            option.options_group = self
            option.save()

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
        
    def get_chart_as_dict(self, site_id=None):

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
        chart_options_group = {}
        if self.chart_options_group:
            chart_options_group = self.chart_options_group.get_as_dict().get('options', None)
        chart_specific_options = self.get_options_as_dict()

        # Append Child datasets and axes
        # -------------------
        for other_dataset in child_datasets:
            _datasets, _x_labels, _x_axis, _y_axis = other_dataset.get_as_dict()
            datasets += _datasets      # Append datasets so last is printed last
            if not x_labels:
                x_labels = _x_labels   # If no labels already specified, use first available
            x_axes += _x_axis
            y_axes += _y_axis

        # Remove multiple references to same axes
        # -----------------------------------
        x_axes = get_unique_list(x_axes)
        y_axes = get_unique_list(y_axes)

        # Add common data to final Dictionary
        # -----------------------------------
        chart_dict = {}
        chart_dict['type'] = self.chart_type

        # Apply Chart colors indexed by dataset
        # -----------------------------------
        # Chart Colors
        self.apply_colors(datasets)
        # Global Colors
        global_colors = GlobalOptionsGroupModel.get_global_colors(site_id)
        if global_colors:
            self.apply_colors(datasets, global_colors)
        # Append Dataset
        chart_dict['data'] = {'datasets': datasets}

        # Get X Labels
        # -------------------
        if x_labels:
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
            options_dict.update({
                'title': {
                    'display': self.display_title,
                    'text': self.label,
                }
            })

        # Add Legend display and position
        # -------------------
        options_dict.update({
            "legend": {
                "display": self.display_legend,
                "position": self.legend_position,
            }
        })

        # Add/override custom options
        # -------------------
        if chart_options_group:
            options_dict.update(chart_options_group)

        # Update Specific Options over any others
        # -------------------
        options_dict.update(chart_specific_options.get('options', {}))

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

