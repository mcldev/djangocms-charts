import json
from django.db import models
from django.utils.translation import ugettext_lazy as _
import djangocms_charts.cache as charts_cache


class ColorModel(models.Model):
    # Multiple choice fields
    types = models.TextField(_('Select the Chart Types'))
    labels = models.TextField(_('Select the Namespace Labels'))
    colors = models.TextField(_('Select Multiple Colors'))

    color_group = models.ForeignKey('ColorGroupModel', on_delete=models.CASCADE, related_name='colors')

    def get_types(self):
        if self.types:
            return json.loads(self.types.replace("'", '"'))

    def get_labels(self):
        if self.labels:
            return json.loads(self.labels.replace("'", '"'))

    def get_colors(self):
        if self.colors:
            return self.colors.split(',')
        return []

class ColorGroupModel(models.Model):
    name = models.CharField(_('Color Group Name'), max_length=100)

    def __str__(self):
        return self.name

    def get_as_dict(self):
        color_dict = {}
        for color in self.colors.all():
            for chart_type in color.get_types():
                chart_color_dict = color_dict.setdefault(chart_type, {})
                for label in color.get_labels():
                    label_colors = chart_color_dict.setdefault(label, [])
                    label_colors += color.get_colors()

        return color_dict

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        charts_cache.clear_all()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        charts_cache.clear_all()

    class Meta:
        verbose_name = 'Color Groups'
        verbose_name_plural = 'Color Groups'
