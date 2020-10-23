
from django.db import migrations, models
import warnings
import json
from djangocms_charts.migration_utils import migrate_cms_plugin, fetch_rows_as_dict

models_to_migrate = [
    'ChartJsBarModel',
    'ChartJsDoughnutModel',
    'ChartJsLineModel',
    'ChartJsPieModel',
    'ChartJsPolarModel',
    'ChartJsRadarModel',
]


chart_option_fields = {
    # {'option_old_field': (new_chart_options_key, new_type, convert_func, ignore_if_equals)...}
    'option_animateRotate': ('options.animation.animateRotate', 'boolean', None, True),
    'option_animateScale': ('options.animation.animateScale', 'boolean', None, False),
    'option_animationEasing': ('options.animation.easing', 'text', None, "easeOutBounce"),
    'option_percentageInnerCutout': ('options.cutoutPercentage', 'number', None, 0),
    'option_segmentStrokeColor': ('options.elements.arc.borderColor', 'text', None, "#fff"),
    'option_segmentStrokeWidth': ('options.elements.arc.borderWidth', 'number', None, 2),
    'option_datasetFill': ('options.elements.line.fill', 'boolean', None, True),
    'option_bezierCurveTension': ('options.elements.line.tension', 'number', None, 0.4),
    'option_pointDotStrokeWidth': ('options.elements.point.borderWidth', 'number', None, 1),
    'option_pointHitDetectionRadius': ('options.elements.point.hitRadius', 'number', None, 20),
    'option_pointDotRadius': ('options.elements.point.radius', 'number', None, 3),
    'option_barStrokeWidth': ('options.elements.rectangle.borderWidth', 'number', None, 2),
    'option_angleLineColor': ('options.scale.angleLines.color', 'text', None, "rgba(0,0,0,.1)"),
    'option_angleShowLineOut': ('options.scale.angleLines.display', 'boolean', None, True),
    'option_angleLineWidth': ('options.scale.angleLines.lineWidth', 'number', None, 1),
    'option_scaleShowLine': ('options.scale.display', 'boolean', None, True),
    'option_scaleGridLineColor': ('options.scale.gridLines.color', 'text', None, "rgba(0,0,0,.05)"),
    'option_scaleShowGridLines': ('options.scale.gridLines.display', 'boolean', None, True),
    'option_scaleGridLineWidth': ('options.scale.gridLines.lineWidth', 'number', None, 1),
    'option_scaleShowLabels': ('options.scale.scaleLabel.display', 'boolean', None, False),
    'option_scaleBeginAtZero': ('options.scale.ticks.beginAtZero', 'boolean', None, True),
    'option_pointLabelFontColor': ('options.tooltips.bodyFontColor', 'text', None, "#666"),
    'option_pointLabelFontFamily': ('options.tooltips.bodyFontFamily', 'text', None, "'Arial'"),
    'option_pointLabelFontSize': ('options.tooltips.bodyFontSize', 'number', None, 10),
    'option_pointLabelFontStyle': ('options.tooltips.bodyFontStyle', 'text', None, "normal"),
}

def save_chart_options(old_plugin_data, apps):
    ChartSpecificOptionsModel = apps.get_model('djangocms_charts', 'chartspecificoptionsmodel')
    # For each Row
    for row in old_plugin_data:
        cms_ptr_id = row['cmsplugin_ptr_id']

        # For each mapped Column
        for old_field, new_opts in chart_option_fields.items():
            if old_field not in row:
                continue

            # Old Value
            old_value = row[old_field]

            # New Values
            new_label = new_opts[0]
            new_type= new_opts[1]
            convert_func = new_opts[2]
            ignore_value = new_opts[3]

            # Ignore value if it is missing or the original default
            if old_value is None or (ignore_value is not None and old_value == ignore_value):
                continue

            new_value = convert_func(old_value) if convert_func else old_value

            new_chart_option = ChartSpecificOptionsModel(label=new_label,
                                                         type=new_type,
                                                         value=new_value,
                                                         options_group_id=cms_ptr_id)
            new_chart_option.save()


def migrate_chart_options(apps, schema_editor):
    for old_app in models_to_migrate:
        old_table = f'djangocms_charts_{old_app.lower()}'
        old_chart_dict = fetch_rows_as_dict(table_name=old_table)
        save_chart_options(old_chart_dict, apps)


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_charts', '0006_migrate_old_chart_data'),
    ]

    operations = [
        migrations.RunPython(migrate_chart_options, reverse_code=migrations.RunPython.noop)
    ]
