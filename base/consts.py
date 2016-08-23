from django.utils.translation import ugettext_lazy as _

# Legend Position
def get_legend_class(position):
    return 'legend-' + str(position)


class LEGEND_POSITIONS:
    BOTTOM = _('bottom')
    TOP = _('top')
    LEFT = _('left')
    RIGHT = _('right')

    get_choices = ((get_legend_class(BOTTOM), BOTTOM),
                   (get_legend_class(TOP), TOP),
                   (get_legend_class(LEFT), LEFT),
                   (get_legend_class(RIGHT), RIGHT),)


def get_chart_position_class(position):
    return 'chart-' + str(position)


class CHART_POSITIONS:
    CENTER = _('center')
    LEFT = _('left')
    RIGHT = _('right')

    get_choices = ((get_chart_position_class(CENTER), CENTER),
                   (get_chart_position_class(LEFT), LEFT),
                   (get_chart_position_class(RIGHT), RIGHT),)