from django.db import migrations
from djangocms_charts.consts import CHART_TYPES

# ------------------------------------------

# Opinionated update for ChartJS
#   - removes height/width and makes Globally Responsive

# ------------------------------------------


def get_color_by_dataset_default(chart_type):
    if chart_type in [CHART_TYPES.LINE, CHART_TYPES.LINE_XY,
                      CHART_TYPES.RADAR, CHART_TYPES.SCATTER, CHART_TYPES.BUBBLE]:
        return True
    if chart_type in [CHART_TYPES.BAR, CHART_TYPES.HORIZONTAL_BAR,
                      CHART_TYPES.DOUGHNUT, CHART_TYPES.PIE, CHART_TYPES.POLAR]:
        return False



def update_color_by_dataset(apps, schema_editor):

    ChartModel = apps.get_model('djangocms_charts', 'chartmodel')

    # Remove chart_width/height from all charts
    charts = ChartModel.objects.all()
    for chart in charts:
        chart.color_by_dataset = get_color_by_dataset_default(chart.type)
        chart.save()




class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_charts', '0007_migrate_old_chart_options'),
    ]

    operations = [
        migrations.RunPython(update_color_by_dataset, reverse_code=migrations.RunPython.noop)
    ]
