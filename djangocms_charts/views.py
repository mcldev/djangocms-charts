from cms.models import CMSPlugin
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404

from djangocms_charts.models import ChartModel, GlobalOptionsGroupModel


def get_chart_as_json(request, chart_id):
    chart_obj = get_object_or_404(ChartModel, id=chart_id)
    qs = CMSPlugin.objects.filter(parent_id=chart_id).order_by('placeholder', 'position')
    chart_obj.child_plugin_instances = [p.get_plugin_instance()[0] for p in qs]
    return JsonResponse(chart_obj.get_chart_as_dict())


def get_global_options_as_json(request, options_id):
    global_options_obj = get_object_or_404(GlobalOptionsGroupModel, id=options_id)
    if not global_options_obj.enabled:
        raise Http404(f'Error - Global Options: {options_id} is not enabled')
    global_opts_dict = {'global_options': global_options_obj.get_as_list()}
    return JsonResponse(global_opts_dict)
