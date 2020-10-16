import json

from django.db import models
from django.utils.translation import ugettext_lazy as _

from djangocms_charts.consts import *
from djangocms_charts.utils import transpose

import djangocms_charts.cache as charts_cache


class DatasetBase(models.Model):

    """
    Dataset Mixin
    """
    label = models.CharField(_("Name"), max_length=256, blank=True, null=True)
    type = models.CharField(_("Chart Type"), max_length=50, choices=CHART_TYPES.get_choices)

    # Table data
    table_data = models.TextField(_("Chart Table data"), blank=True)

    # Set Data Input Options
    labels_top = models.BooleanField(_("Labels top row"), default=True)
    labels_left = models.BooleanField(_("Labels left column"), default=True)
    data_series_format = models.CharField(_("Multiple Datasets in Rows or Columns"), max_length=10,
                                          default='rows', choices=DATASET_FORMATS)

    # Set Options and Axes
    options = models.ForeignKey('DatasetOptionsGroupModel', on_delete=models.CASCADE, related_name="%(class)s_options", blank=True, null=True)
    xAxis = models.ForeignKey('AxisModel', on_delete=models.CASCADE, related_name="%(class)s_xAxis", blank=True, null=True)
    yAxis = models.ForeignKey('AxisModel', on_delete=models.CASCADE, related_name="%(class)s_yAxis", blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        charts_cache.clear_all()

    class Meta:
        """Abstract model."""
        abstract = True

    @property
    def chart_type(self):
        return CHART_TYPES.LINE if self.type == CHART_TYPES.LINE_XY else self.type

    DEFAULT_SCALAR_AXES = {
        # https://stackoverflow.com/a/57130191/12400711
        "type": "linear",   # MANDATORY TO SHOW YOUR POINTS! (THIS IS THE IMPORTANT BIT)
        "display": True,    # mandatory
        "position": 'bottom',
        "scaleLabel": {
            "display": True, # mandatory
        },
    }

    def get_as_dict(self):
        # Get Datasets
        datasets = self.get_datasets()

        # Get X Labels
        x_labels = self.get_x_labels()

        # Get Axes
        x_axes = [self.xAxis.get_as_dict()] if self.xAxis else []
        if not x_axes and self.type == CHART_TYPES.LINE_XY:
            x_axes = [self.DEFAULT_SCALAR_AXES]
        y_axes = [self.yAxis.get_as_dict()] if self.yAxis else []

        return datasets, x_labels, x_axes, y_axes


    # DATA FORMATS:
    # ------------
    #
    # LABELS + VALUE TYPES:
    #
    # Line:
    # -----
    #     type: 'line',
    #     data: {
    #         labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    #         datasets: [{
    #             data: [20, 50, 100, 75, 25, 0],
    #             label: 'Left dataset',
    #
    #             // This binds the dataset to the left y axis
    #             yAxisID: 'left-y-axis'
    #         }, {
    #             data: [0.1, 0.5, 1.0, 2.0, 1.5, 0],
    #             label: 'Right dataset',
    #
    #             // This binds the dataset to the right y axis
    #             yAxisID: 'right-y-axis'
    #         }],
    #     },
    #
    # Bar:
    # ----
    # data: {
    #     datasets: [{
    #         data: [10, 20, 30, 40, 50, 60, 70],
    #         label: 'Bar dataset'
    #     }],
    #     labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    # };
    #
    # Radar:
    # ------
    # data: {
    #     datasets: [{
    #         data: [20, 10, 4, 2]
    #     }],
    #     labels: ['Running', 'Swimming', 'Eating', 'Cycling']
    # }
    #
    # Doughnut/Pie:
    # -------------
    # data = {
    #     datasets: [{
    #         data: [10, 20, 30]
    #     }],
    #
    #     // These labels appear in the legend and in the tooltips when hovering different arcs
    #     labels: ['Red', 'Yellow', 'Blue']
    # };
    #
    # PolarArea:
    # ----------
    # data = {
    #     datasets: [{
    #         data: [10, 20, 30]
    #     }],
    #
    #     // These labels appear in the legend and in the tooltips when hovering different arcs
    #     labels: ['Red', 'Yellow', 'Blue']
    # };
    #
    #
    # COORDINATE + VALUE TYPES:
    #
    # Bubble:
    # ----------
    # type: 'bubble',
    # data: {
    #     datasets: [{
    #         label: 'Bubble Dataset',
    #         data: [{
    #               // X Value
    #               x: number,
    #
    #               // Y Value
    #               y: number,
    #
    #               // Bubble radius in pixels (not scaled).
    #               r: number
    #               }, ...]
    #     }],
    #      labels: ['Red', 'Yellow', 'Blue']
    # };
    #
    # Scatter / Line_XY
    # --------
    #     type: 'scatter',  OR 'line'
    #     data: {
    #         datasets: [{
    #             label: 'Scatter Dataset',
    #             data: [{
    #                 x: -10,
    #                 y: 0
    #             }, {
    #                 x: 0,
    #                 y: 10
    #             }, {
    #                 x: 10,
    #                 y: 5
    #             }]
    #         }]
    #     },
    #     options: {
    #         scales: {
    #             xAxes: [{
    #                 type: 'linear',
    #                 position: 'bottom'
    #             }]
    #         }
    #     }


    # INPUT DATA:
    # -----------
    #
    # Line, Bar, Radar, Doughnut, Pie, PolarArea
    # ------------------------------------------
    # Datasets in 'cols' > TRANSPOSED
    #       Label_1,    Label_2, ...
    # Jan-20    10      30
    # Feb-20    20      40
    # ...
    #
    # OR
    #
    # Datasets in 'rows'    > USE THIS FORMAT INTERNALLY
    #       Jan-20      Feb-20, ...
    # Label_1   10      20
    # Label_2   30      40
    # ...
    #
    # Bubble [r], Scatter, Line_XY
    # ----------------------------
    # [r - radius - is ignored for line and scatter]
    #
    # Datasets in 'cols' > TRANSPOSED
    #   x   10   20     ...
    #   y   30   40     ...
    #  [r]   5   10     ...
    #
    # OR
    #
    # Datasets in 'rows'    > USE THIS FORMAT INTERNALLY
    #   x,      y,      [r]
    #   10      30      5
    #   20      40      10
    #   ...
    #

    def _init_data(self):
        if hasattr(self, '_table_data'):
            return

        #If Table data is a string (as saved by django) then load it as array.
        table_data = json.loads(self.table_data) if \
            isinstance(self.table_data, str) else self.table_data

        # Switch top/left if data is transposed
        self._data_series_in_rows = (self.data_series_format == 'rows')
        if self._data_series_in_rows:
            self._has_x_labels = int(self.labels_top)
            self._has_data_labels = int(self.labels_left)
            self._table_data = table_data
        else:
            self._has_data_labels = int(self.labels_top)
            self._has_x_labels = int(self.labels_left)
            self._table_data = transpose(table_data)


    # Get X Labels as list, or None
    def get_x_labels(self):
        self._init_data()
        if not self._table_data:
            return []
        if CHART_TYPES.is_coordinate_type(self.type):
            return []
        # Get the X Axes Labels or Categories
        if self._has_x_labels:
            return self._table_data[0][self._has_data_labels:]


    # Get Data as List
    def get_datasets(self):
        # Init and format data
        self._init_data()
        if not self._table_data:
            return []

        # Get datasets as list of dicts
        if CHART_TYPES.is_coordinate_type(self.type):
            datasets = self._get_datasets_as_coordinate_values()
        else:
            datasets = self._get_datasets_as_labels_values()

        # Append common information
        for dataset in datasets:
            # Add dataset type, redundant for main chart
            dataset['type'] = self.chart_type
            # Add dataset options if included
            if self.options:
                dataset.update(self.options.get_as_dict())
            if self.xAxis:
                dataset['xAxisID'] = self.xAxis.slug
            # if self.yAxis:
            #     dataset['yAxisID'] = self.yAxis.slug

        return datasets


    def _get_datasets_as_labels_values(self):
        datasets = []
        for r in range(self._has_x_labels, len(self._table_data)):
            dataset = {}
            if self._has_data_labels:
                dataset['label'] = self._table_data[r][0]
            elif self.label:
                dataset['label'] = self.label
            dataset['data'] = self._table_data[r][self._has_data_labels:]
            datasets.append(dataset)

        return datasets


    def _get_datasets_as_coordinate_values(self):
        # Get the X Axes Labels or Categories
        if self._has_x_labels:
            labels = self._table_data[0][self._has_data_labels:]
        else:
            # trim to x, y or x, y, r
            labels = ['x', 'y', 'r'][:len(self._table_data[0][self._has_data_labels:])]

        # Build unique datasets on the dataset label or each row label if provided
        all_datasets = {}
        for r in range(self._has_x_labels, len(self._table_data)):
            # Get label from first col (if set) or from dataset label
            label = self._table_data[r][0] if self._has_data_labels else self.label
            # Get or set the default data as a list
            data_list = all_datasets.setdefault(label, [])
            # Create the coordinate dictionary based on the labels {'x': 1, 'y':2}
            data_list.append({labels[i]: self._table_data[r][i + self._has_data_labels]
                              for i in range(len(labels))})

        # Format as data dictionary
        datasets = []
        for label, data_list in all_datasets.items():
            dataset = {}
            dataset['label'] = label
            dataset['data'] = data_list
            datasets.append(dataset)

        return datasets



