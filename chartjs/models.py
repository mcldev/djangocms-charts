from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangocms_charts.base.models import ChartsBaseModel
from .consts import *


class ChartJsBaseModel(ChartsBaseModel):
    # Put in any other settings common only to ChartJs models
    # chart_type = None

    # Need to push the chart_type back down to the parent class... as there is no self:: static method for parent classes...
    def __init__(self, *args, **kwargs):
        super(ChartJsBaseModel, self).__init__(*args, **kwargs)
        ChartsBaseModel.chart_type = self.chart_type

    class Meta:
        abstract = True


class ChartJsLineModel(ChartJsBaseModel):
    chart_type = CHART_TYPES.LINE

    # Boolean - Whether grid lines are shown across the chart
    option_scaleShowGridLines = models.BooleanField(_("Grid lines are shown across the chart"), blank=True, default=True)

    # String - Colour of the grid lines
    option_scaleGridLineColor = models.CharField(_("Colour of the grid lines"), max_length=300, blank=True, default="rgba(0,0,0,.05)")

    # Number - Width of the grid lines
    option_scaleGridLineWidth = models.IntegerField(_("Width of the grid lines"), null=True, blank=True, default=1)

    # Boolean - Whether to show horizontal lines (except X axis)
    option_scaleShowHorizontalLines = models.BooleanField(_("Show horizontal lines (except X axis)"), blank=True, default=True)

    # Boolean - Whether to show vertical lines (except Y axis)
    option_scaleShowVerticalLines = models.BooleanField(_("Show vertical lines (except Y axis)"), blank=True, default=True)

    # Boolean - Whether the line is curved between points
    option_bezierCurve = models.BooleanField(_("Line is curved between points"), blank=True, default=True)

    # Number - Tension of the bezier curve between points
    option_bezierCurveTension = models.FloatField(_("Tension of the bezier curve between points"), null=True, blank=True, default=0.4)

    # Boolean - Whether to show a dot for each point
    option_pointDot = models.BooleanField(_("Show a dot for each point"), blank=True, default=True)

    # Number - Radius of each point dot in pixels
    option_pointDotRadius = models.IntegerField(_("Radius of each point dot in pixels"), null=True, blank=True, default=4)

    # Number - Pixel width of point dot stroke
    option_pointDotStrokeWidth = models.IntegerField(_("Pixel width of point dot stroke"), null=True, blank=True, default=1)

    # Number - amount extra to add to the radius to cater for hit detection outside the drawn point
    option_pointHitDetectionRadius = models.IntegerField(_("Amount extra to add to the radius to cater for hit detection outside the drawn point"), null=True, blank=True, default=20)

    # Boolean - Whether to show a stroke for datasets
    option_datasetStroke = models.BooleanField(_("Show a stroke for datasets"), blank=True, default=True)

    # Number - Pixel width of dataset stroke
    option_datasetStrokeWidth = models.IntegerField(_("Pixel width of dataset stroke"), null=True, blank=True, default=2)

    # Boolean - Whether to fill the dataset with a colour
    option_datasetFill = models.BooleanField(_("Fill the dataset with a colour"), blank=True, default=True)

    # String - A legend template
    option_legendTemplate = models.CharField(_("A legend template"), max_length=300, blank=True, default="<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>")


class ChartJsBarModel(ChartJsBaseModel):
    chart_type = CHART_TYPES.BAR

    # Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
    option_scaleBeginAtZero = models.BooleanField(_("Scale should start at zero, or an order of magnitude down from the lowest value"), blank=True, default=True)

    # Boolean - Whether grid lines are shown across the chart
    option_scaleShowGridLines = models.BooleanField(_("Grid lines are shown across the chart"), blank=True, default=True)

    # String - Colour of the grid lines
    option_scaleGridLineColor = models.CharField(_("Colour of the grid lines"), max_length=300, blank=True, default="rgba(0,0,0,.05)")

    # Number - Width of the grid lines
    option_scaleGridLineWidth = models.IntegerField(_("Width of the grid lines"), null=True, blank=True, default=1)

    # Boolean - Whether to show horizontal lines (except X axis)
    option_scaleShowHorizontalLines = models.BooleanField(_("Show horizontal lines (except X axis)"), blank=True, default=True)

    # Boolean - Whether to show vertical lines (except Y axis)
    option_scaleShowVerticalLines = models.BooleanField(_("Show vertical lines (except Y axis)"), blank=True, default=True)

    # Boolean - If there is a stroke on each bar
    option_barShowStroke = models.BooleanField(_("Stroke on each bar"), blank=True, default=True)

    # Number - Pixel width of the bar stroke
    option_barStrokeWidth = models.IntegerField(_("Pixel width of the bar stroke"), null=True, blank=True, default=2)

    # Number - Spacing between each of the X value sets
    option_barValueSpacing = models.IntegerField(_("Spacing between each of the X value sets"), null=True, blank=True, default=5)

    # Number - Spacing between data sets within X values
    option_barDatasetSpacing = models.IntegerField(_("Spacing between data sets within X values"), null=True, blank=True, default=1)

    # String - A legend template
    option_legendTemplate = models.CharField(_("Legend template"), max_length=300, blank=True, default="<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].fillColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>")


class ChartJsRadarModel(ChartJsBaseModel):
    chart_type = CHART_TYPES.RADAR

    # Boolean - Whether to show lines for each scale point
    option_scaleShowLine = models.BooleanField(_("Show lines for each scale point"), blank=True, default=True)

    # Boolean - Whether we show the angle lines out of the radar
    option_angleShowLineOut = models.BooleanField(_("Show the angle lines out of the radar"), blank=True, default=True)

    # Boolean - Whether to show labels on the scale
    option_scaleShowLabels = models.BooleanField(_("Show labels on the scale"), blank=True, default=False)

    #  Boolean - Whether the scale should begin at zero
    option_scaleBeginAtZero = models.BooleanField(_("Scale should begin at zero"), blank=True, default=True)

    # String - Colour of the angle line
    option_angleLineColor = models.CharField(_("Colour of the angle line"), max_length=300, blank=True, default="rgba(0,0,0,.1)")

    # Number - Pixel width of the angle line
    option_angleLineWidth = models.IntegerField(_("Pixel width of the angle line"), null=True, blank=True, default=1)

    # String - Point label font declaration
    option_pointLabelFontFamily = models.CharField(_("Point label font declaration"), max_length=300, blank=True, default="'Arial'")

    # String - Point label font weight
    option_pointLabelFontStyle = models.CharField(_("Point label font weight"), max_length=300, blank=True, default="normal")

    # Number - Point label font size in pixels
    option_pointLabelFontSize = models.IntegerField(_("Point label font size in pixels"), null=True, blank=True, default=10)

    # String - Point label font colour
    option_pointLabelFontColor = models.CharField(_("Point label font colour"), max_length=300, blank=True, default="#666")

    # Boolean - Whether to show a dot for each point
    option_pointDot = models.BooleanField(_("Show a dot for each point"), blank=True, default=True)

    # Number - Radius of each point dot in pixels
    option_pointDotRadius = models.IntegerField(_("Radius of each point dot in pixels"), null=True, blank=True, default=3)

    # Number - Pixel width of point dot stroke
    option_pointDotStrokeWidth = models.IntegerField(_("Pixel width of point dot stroke"), null=True, blank=True, default=1)

    # Number - amount extra to add to the radius to cater for hit detection outside the drawn point
    option_pointHitDetectionRadius = models.IntegerField(_("amount extra to add to the radius to cater for hit detection outside the drawn point"), null=True, blank=True, default=20)

    # Boolean - Whether to show a stroke for datasets
    option_datasetStroke = models.BooleanField(_("Show a stroke for datasets"), blank=True, default=True)

    # Number - Pixel width of dataset stroke
    option_datasetStrokeWidth = models.IntegerField(_("Pixel width of dataset stroke"), null=True, blank=True, default=2)

    # Boolean - Whether to fill the dataset with a colour
    option_datasetFill = models.BooleanField(_("Fill the dataset with a colour"), blank=True, default=True)

    # String - A legend template
    option_legendTemplate = models.CharField(_("Legend template"), max_length=300, blank=True, default="<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>")


class ChartJsPolarModel(ChartJsBaseModel):
    chart_type = CHART_TYPES.POLAR

    # Boolean - Show a backdrop to the scale label
    option_scaleShowLabelBackdrop = models.BooleanField(_("Show a backdrop to the scale label"), blank=True, default=True)

    # String - The colour of the label backdrop
    option_scaleBackdropColor = models.CharField(_("The colour of the label backdrop"), max_length=300, blank=True, default="rgba(255,255,255,0.75)")

    #  Boolean - Whether the scale should begin at zero
    option_scaleBeginAtZero = models.BooleanField(_("Scale should begin at zero"), blank=True, default=True)

    # Number - The backdrop padding above & below the label in pixels
    option_scaleBackdropPaddingY = models.IntegerField(_("The backdrop padding above & below the label in pixels"), null=True, blank=True, default=2)

    # Number - The backdrop padding to the side of the label in pixels
    option_scaleBackdropPaddingX = models.IntegerField(_("The backdrop padding to the side of the label in pixels"), null=True, blank=True, default=2)

    # Boolean - Show line for each value in the scale
    option_scaleShowLine = models.BooleanField(_("Show line for each value in the scale"), blank=True, default=True)

    # Boolean - Stroke a line around each segment in the chart
    option_segmentShowStroke = models.BooleanField(_("Stroke a line around each segment in the chart"), blank=True, default=True)

    # String - The colour of the stroke on each segement.
    option_segmentStrokeColor = models.CharField(_("The colour of the stroke on each segement."), max_length=300, blank=True, default="#fff")

    # Number - The width of the stroke value in pixels
    option_segmentStrokeWidth = models.IntegerField(_("The width of the stroke value in pixels"), null=True, blank=True, default=2)

    # Number - Amount of animation steps
    option_animationSteps = models.IntegerField(_("Amount of animation steps"), null=True, blank=True, default=100)

    # String - Animation easing effect.
    option_animationEasing = models.CharField(_("Animation easing effect."), max_length=300, blank=True, default="easeOutBounce")

    # Boolean - Whether to animate the rotation of the chart
    option_animateRotate = models.BooleanField(_("Animate the rotation of the chart"), blank=True, default=True)

    # Boolean - Whether to animate scaling the chart from the centre
    option_animateScale = models.BooleanField(_("Animate scaling the chart from the centre"), blank=True, default=False)

    # String - A legend template
    option_legendTemplate = models.CharField(_("A legend template"), max_length=300, blank=True, default="<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>")


class ChartJsDougnutPieModel(ChartJsBaseModel):

    # Boolean - Whether we should show a stroke on each segment
    option_segmentShowStroke = models.BooleanField(_("Show a stroke on each segment"), blank=True, default=True)

    # String - The colour of each segment stroke
    option_segmentStrokeColor = models.CharField(_("The colour of each segment stroke"), max_length=300, blank=True, default="#fff")

    # Number - The width of each segment stroke
    option_segmentStrokeWidth = models.IntegerField(_("The width of each segment stroke"), null=True, blank=True, default=2)

    # Number - Amount of animation steps
    option_animationSteps = models.IntegerField(_("Amount of animation steps"), null=True, blank=True, default=100)

    # String - Animation easing effect
    option_animationEasing = models.CharField(_("Animation easing effect"), max_length=300, blank=True, default="easeOutBounce")

    # Boolean - Whether we animate the rotation of the Doughnut
    option_animateRotate = models.BooleanField(_("Animate the rotation of the Chart"), blank=True, default=True)

    # Boolean - Whether we animate scaling the Doughnut from the centre
    option_animateScale = models.BooleanField(_("Animate scaling the Doughnut from the centre"), blank=True, default=False)

    # String - A legend template
    option_legendTemplate = models.CharField(_("Legend template"), max_length=300, blank=True, default="<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>")

    class Meta:
        abstract = True

class ChartJsPieModel(ChartJsDougnutPieModel):
    chart_type = CHART_TYPES.PIE

    # Number - The percentage of the chart that we cut out of the middle
    option_percentageInnerCutout = models.IntegerField(_("The percentage of the chart that we cut out of the middle"), null=True, blank=True, default=0)

    pass

class ChartJsDoughnutModel(ChartJsDougnutPieModel):
    chart_type = CHART_TYPES.DOUGHNUT

    # Number - The percentage of the chart that we cut out of the middle
    option_percentageInnerCutout = models.IntegerField(_("The percentage of the chart that we cut out of the middle"), null=True, blank=True, default=50)

    pass