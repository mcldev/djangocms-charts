import json

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

import djangocms_charts.cache as charts_cache
from .models_options import OptionsGroupBase, OptionsBase
from .consts import AXIS_TYPES, AXIS_DISPLAY


# Axis Options Model
# --------------------------------------

class AxisOptionsModel(OptionsBase):
    options_group = models.ForeignKey('AxisOptionsGroupModel', on_delete=models.CASCADE, related_name='options')


class AxisOptionsGroupModel(OptionsGroupBase):
    # data: {
    #         labels: ['January', 'February', 'March', 'April', 'May', 'June'],
    #         datasets: [{
    #             // This dataset appears on the first axis
    #             yAxisID: 'first-y-axis'
    #         }, {
    #             // This dataset appears on the second axis
    #             yAxisID: 'second-y-axis'
    #         }]
    #     },
    # options: {
    #         scales: {
    #             yAxes: [{
    #                 id: 'left-y-axis',
    #                 type: 'linear',
    #                 position: 'left'
    #             }, {
    #                 id: 'right-y-axis',
    #                 type: 'linear',
    #                 position: 'right'
    #             }],
    #             xAxes: [{
    #                 type: 'category',
    #                 labels: ['January', 'February', 'March', 'April', 'May', 'June']
    #             }]
    #         }
    #     }
    # Radial:
    # -------
    # options: {
    #         scale: {
    #             ticks: {
    #                 suggestedMin: 50,
    #                 suggestedMax: 100
    #             }
    #         }
    #     }
    #
    # Stacked Area Chart:
    # ------------------
    #     type: 'line',
    #     data: data,
    #     options: {
    #         scales: {
    #             yAxes: [{
    #                 stacked: true
    #             }]
    #         }
    #     }

    type = models.CharField(_("Axis Type"), max_length=30, choices=AXIS_TYPES, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    display = models.CharField(_('display'), help_text=_(
        'Controls the axis global visibility (visible when true, hidden when false). '
        'When display: auto, the axis is visible only if at least one associated dataset is visible.'),
                               max_length=100, blank=True, null=True, choices=AXIS_DISPLAY)
    weight = models.IntegerField(_('weight'), help_text=_(
        'The weight used to sort the axis. Higher weights are further away from the chart area.'), null=True,
                                 blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = slugify(f'{self.id}_{self.name}')
        super().save(*args, **kwargs)
        charts_cache.clear_all()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        charts_cache.clear_all()

    def get_axis_as_dict(self, x_or_y):
        axis_dict = {}
        axis_dict['id'] = self.get_axis_id(x_or_y)
        if self.type:
            axis_dict['type'] = self.type
        if self.display:
            axis_dict['display'] = json.loads(self.display)
        if self.weight:
            axis_dict['weight'] = self.weight
        options = super(AxisOptionsGroupModel, self).get_as_dict()
        if options:
            axis_dict.update(options)
        return axis_dict

    def get_axis_id(self, x_or_y):
        return slugify(f'{x_or_y}_{self.slug}')

    # Axis Name
    def __str__(self):
        if self.type:
            return str(f'{self.name or self.id} [{self.type}]')
        return str(f'{self.name or self.id}')

