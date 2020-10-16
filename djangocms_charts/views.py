
from cms.utils.moderator import get_cmsplugin_queryset
from cms.utils.plugins import build_plugin_tree
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404

from djangocms_charts.models import ChartModel, GlobalOptionsGroupModel


def get_chart_as_json(request, chart_id):
    chart_obj = get_object_or_404(ChartModel, id=chart_id)

    # Get the CMSPlugins of Dataset Children if any
    qs = get_cmsplugin_queryset()
    qs = qs.filter(Q(parent_id=chart_id))

    # For some reason we need position not path here...
    plugins = list(qs.order_by('placeholder', 'position'))
    datasets = [p.get_plugin_instance()[0] for p in plugins]

    # Set Child objects
    chart_obj.child_plugin_instances = datasets
    return JsonResponse(chart_obj.get_chart_as_dict())


def get_global_options_as_json(request, options_id):
    global_options_obj = get_object_or_404(GlobalOptionsGroupModel, id=options_id)
    if not global_options_obj.enabled:
        return Http404(f'Error - Global Options: {options_id} is not enabled')
    global_opts_dict = {'global_options': global_options_obj.get_as_list()}
    return JsonResponse(global_opts_dict)
