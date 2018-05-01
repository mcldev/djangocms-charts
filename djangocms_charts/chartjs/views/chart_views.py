from djangocms_charts.base.views.chart_view import BaseChartView
from djangocms_charts.chartjs.consts import *

class ChartJsView(BaseChartView):

    # Main function to return JSON data - overwriting ContextMixin
    # -------------------
    def get_context_data(self):

        # Return a data array with either a dataset, label/value pairs
        dataset_type = DATA_LABELS.VALUE if self.get_chart_type() in CHART_TYPES.get_label_value_types else DATA_LABELS.DATASET

        if dataset_type == DATA_LABELS.DATASET:
            data = self._build_dataset()
        else:
            data = self._build_data()

        return data

    # Build Dataset type values - Line, Bar, Radar etc
    # -------------------
    def _build_dataset(self):

        # Data array is the return object
        data = {}

        # Try to get the series data labels if present
        try:
            series_labels = self.get_series_labels()
        except:
            series_labels = None

        # Data is inserted into the Datasets
        datasets = []
        get_data = self.get_data()
        for i, the_data in enumerate(get_data):
            # Add Labels if present
            if series_labels :
                dataset = {DATA_LABELS.LABEL: series_labels[i],
                           DATA_LABELS.DATA: the_data}
            else:
                dataset = {DATA_LABELS.DATA: the_data}

            # Append to the dataset
            datasets.append(dataset)

        # Add Data and X-Axis Labels
        if self.get_labels() :
            data[DATA_LABELS.LABELS] = self.get_labels()
        data[DATA_LABELS.DATASET] = datasets

        return data


    # Build Data Array type values (Label, Values) - Pie, Polar etc
    # -------------------
    def _build_data(self):
        # Data array is the return object
        data = []

        # Try to get the series data labels if present, then labels if not
        try:
            series_labels = self.get_series_labels()
        except:
            try:
                series_labels = self.get_labels()
            except:
                series_labels = None

        # Data is inserted into each value/data pair
        get_data = self.get_data()

        for i, the_data in enumerate(get_data):
            # Add Labels if present
            if series_labels:
                dataset = {DATA_LABELS.LABEL: series_labels[i],
                           DATA_LABELS.VALUE: the_data[0]}
            else:
                dataset = {DATA_LABELS.VALUE: the_data[0]}

            # Append to data
            data.append(dataset)

        return data

    # class Meta:
    #     abstract = True