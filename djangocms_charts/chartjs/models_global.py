
from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import Q
from djangocms_charts.utils import get_fields_and_values_from_obj

def get_current_chartjs_global_settings():
    current_site = settings.SITE_ID
    object_query = Q(site_id = current_site)
    return get_fields_and_values_from_obj(ChartJsGlobalSettingsModel, object_query,enable_field='enable')


class ChartJsGlobalSettingsModel(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    # Enable flag to switch global settings on/off
    enable = models.BooleanField(_("Enable Global Settings"), blank=True, default=True)

    name = models.CharField(_('Name'), max_length=250, default='Global ChartJs Settings')

    #  Boolean - Animate the chart	
    animation = models.BooleanField(_("Animate the chart"), blank=True, default=True)

    #  Number - Number of animation steps
    animationSteps = models.IntegerField(_("Number of animation steps"), null=True, blank=True, default=60)

    #  String - Animation easing effect
    animationEasing = models.CharField(_("Animation easing effect"), max_length=300, blank=True, default="easeOutQuart")

    #  Boolean - Show the scale
    showScale = models.BooleanField(_("Show the scale"), blank=True, default=True)

    #  Boolean - Override with a hard coded scale
    scaleOverride = models.BooleanField(_("Override with a hard coded scale"), blank=True, default=False)

    #  Number - Number of steps in a hard coded scale
    scaleSteps = models.IntegerField(_("Number of steps in a hard coded scale"), null=True, blank=True)

    #  Number - Value jump in the hard coded scale
    scaleStepWidth = models.IntegerField(_("Value jump in the hard coded scale"), null=True, blank=True)

    #  Number - Scale starting value
    scaleStartValue = models.IntegerField(_("Scale starting value"), null=True, blank=True)

    #  String - Colour of the scale line
    scaleLineColor = models.CharField(_("Colour of the scale line"), max_length=300, blank=True, default="rgba(0,0,0,0.1)")

    #  Number - Pixel width of the scale line
    scaleLineWidth = models.IntegerField(_("Pixel width of the scale line"), null=True, blank=True, default=1)

    #  Boolean - Show labels on the scale
    scaleShowLabels = models.BooleanField(_("Show labels on the scale"), blank=True, default=True)

    #  String - Display value
    scaleLabel = models.CharField(_("Display value"), max_length=300, blank=True, default="<%=value%>")

    #  Boolean - Scale should stick to integers, not floats
    scaleIntegersOnly = models.BooleanField(_("Scale should stick to integers, not floats"), blank=True, default=True)

    #  Boolean - Scale should start at zero
    scaleBeginAtZero = models.BooleanField(_("Scale should start at zero"), blank=True, default=False)

    #  String - Scale label font declaration for the scale label
    scaleFontFamily = models.CharField(_("Scale label font declaration for the scale label"), max_length=300,
                                       blank=True, default="'Helvetica Neue' 'Helvetica' 'Arial' sans-serif")

    #  Number - Scale label font size in pixels
    scaleFontSize = models.IntegerField(_("Scale label font size in pixels"), null=True, blank=True, default=12)

    #  String - Scale label font weight style
    scaleFontStyle = models.CharField(_("Scale label font weight style"), max_length=300, blank=True, default="normal")

    #  String - Scale label font colour
    scaleFontColor = models.CharField(_("Scale label font colour"), max_length=300, blank=True, default="#666")

    #  Boolean - Chart should be responsive and resize when the browser does.
    responsive = models.BooleanField(_("Chart should be responsive and resize when the browser does."), blank=True,
                                     default=False)

    #  Boolean - Maintain the starting aspect ratio when responsive
    maintainAspectRatio = models.BooleanField(_("Maintain the starting aspect ratio when responsive"), blank=True,
                                              default=True)

    #  Boolean - Draw tooltips on the canvas
    showTooltips = models.BooleanField(_("Draw tooltips on the canvas"), blank=True, default=True)

    #  String - Tooltip background colour
    tooltipFillColor = models.CharField(_("Tooltip background colour"), max_length=300, blank=True,
                                        default="rgba(0,0,0,0.8)")

    #  String - Tooltip label font declaration for the scale label
    tooltipFontFamily = models.CharField(_("Tooltip label font declaration for the scale label"), max_length=300,
                                         blank=True, default="'Helvetica Neue' 'Helvetica' 'Arial' sans-serif")

    #  Number - Tooltip label font size in pixels
    tooltipFontSize = models.IntegerField(_("Tooltip label font size in pixels"), null=True, blank=True, default=14)

    #  String - Tooltip font weight style
    tooltipFontStyle = models.CharField(_("Tooltip font weight style"), max_length=300, blank=True, default="normal")

    #  String - Tooltip label font colour
    tooltipFontColor = models.CharField(_("Tooltip label font colour"), max_length=300, blank=True, default="#fff")

    #  String - Tooltip title font declaration for the scale label
    tooltipTitleFontFamily = models.CharField(_("Tooltip title font declaration for the scale label"), max_length=300,
                                              blank=True, default="'Helvetica Neue' 'Helvetica' 'Arial' sans-serif")

    #  Number - Tooltip title font size in pixels
    tooltipTitleFontSize = models.IntegerField(_("Tooltip title font size in pixels"), null=True, blank=True,
                                               default=14)

    #  String - Tooltip title font weight style
    tooltipTitleFontStyle = models.CharField(_("Tooltip title font weight style"), max_length=300, blank=True,
                                             default="bold")

    #  String - Tooltip title font colour
    tooltipTitleFontColor = models.CharField(_("Tooltip title font colour"), max_length=300, blank=True, default="#fff")

    #  Number - pixel width of padding around tooltip text
    tooltipYPadding = models.IntegerField(_("pixel width of padding around tooltip text"), null=True, blank=True,
                                          default=6)

    #  Number - pixel width of padding around tooltip text
    tooltipXPadding = models.IntegerField(_("pixel width of padding around tooltip text"), null=True, blank=True,
                                          default=6)

    #  Number - Size of the caret on the tooltip
    tooltipCaretSize = models.IntegerField(_("Size of the caret on the tooltip"), null=True, blank=True, default=8)

    #  Number - Pixel radius of the tooltip border
    tooltipCornerRadius = models.IntegerField(_("Pixel radius of the tooltip border"), null=True, blank=True, default=6)

    #  Number - Pixel offset from point x to tooltip edge
    tooltipXOffset = models.IntegerField(_("Pixel offset from point x to tooltip edge"), null=True, blank=True,
                                         default=10)

    #  String - Template string for single tooltips
    tooltipTemplate = models.CharField(_("Template string for single tooltips"), max_length=300, blank=True)

    #  String - Template string for multiple tooltips
    multiTooltipTemplate = models.CharField(_("Template string for multiple tooltips"), max_length=300, blank=True,
                                            default="<%= value %>")


    class Meta:
        verbose_name = 'ChartJs Global Settings'
        verbose_name_plural = 'ChartJs Global Settings'
        ordering = ['name']
