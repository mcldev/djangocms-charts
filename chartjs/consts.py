
# Chart Types
class CHART_TYPES:
    LINE = 'Line'
    BAR = 'Bar'
    RADAR = 'Radar'
    POLAR = 'PolarArea'
    PIE = 'Pie'
    DOUGHNUT = 'Doughnut'

    get_label_value_types= (POLAR,
                            PIE,
                            DOUGHNUT)

    get_choices= ((LINE, LINE),
                (BAR, BAR),
                (RADAR, RADAR),
                (POLAR, POLAR),
                (PIE, PIE),
                (DOUGHNUT, DOUGHNUT),)


# Dataset Labels
class DATA_LABELS:
    DATASET = 'datasets'
    DATA = 'data'
    VALUE = 'value'
    LABEL = 'label'
    LABELS = 'labels'



