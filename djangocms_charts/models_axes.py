import json

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

import djangocms_charts.cache as charts_cache
from .consts import AXIS_TYPES, AXIS_DISPLAY


class AxisModel(models.Model):
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

    label = models.CharField(_("Axis Name"), max_length=256)
    type = models.CharField(_("Axis Type"), max_length=10, choices=AXIS_TYPES)
    slug = models.SlugField(unique=True)

    display = models.CharField(_('display'), help_text=_(
        'Controls the axis global visibility (visible when true, hidden when false). '
        'When display: auto, the axis is visible only if at least one associated dataset is visible.'),
                               max_length=100, blank=True, null=True, choices=AXIS_DISPLAY)
    weight = models.IntegerField(_('weight'), help_text=_(
        'The weight used to sort the axis. Higher weights are further away from the chart area.'), null=True,
                                 blank=True)

    options = models.ForeignKey('AxisOptionsGroupModel', on_delete=models.CASCADE, related_name='axis_options', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.type}_{self.label}')
        super(AxisModel, self).save(*args, **kwargs)
        charts_cache.clear_all()

    def get_as_dict(self):
        axis_dict = {}
        axis_dict['id'] = self.slug
        axis_dict['type'] = self.type
        if self.display:
            axis_dict['display'] = json.loads(self.display)
        if self.weight:
            axis_dict['weight'] = self.weight
        if self.options:
            axis_dict.update(self.options.get_as_dict())

        return axis_dict

    @property
    def axis_name(self):
        get_name = str(f'{self.type}_{self.label or self.id}')
        #  Replace all non-chars
        get_name = slugify(get_name)
        return get_name

    # Axis Name
    def __str__(self):
        return self.axis_name

