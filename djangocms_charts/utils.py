from django.forms.models import model_to_dict
from django.db.models import Q
from six import string_types

def transpose(the_array):
    ret = map(list, zip(*the_array))
    ret = list(ret)
    return ret


# def get_fields_from_obj(obj, filter_fields_lambda=None):
#     # Get all field names
#     field_names = [f.name for f in obj._meta.get_fields()]
#
#     # Filter settings if provided
#     if filter_fields_lambda:
#         field_names = {f for f in field_names if filter_fields_lambda(f)}
#
#     field_names = tuple(field_names)
#
#     return field_names
#
#
# def get_fields_and_values_from_obj(class_obj, obj_query, filter_fields_lambda=None, filter_values_lambda=None,
#                                     convert_fields_lambda = None, convert_values_lambda = None,
#                                     skip_blanks=True, enable_field=None, convert_to_js= True):
#     # Get Chart Data
#     try:
#         settings_obj = class_obj.objects.get(obj_query)
#     except class_obj.DoesNotExist:
#         return None
#
#     return get_fields_and_values_from_instance(settings_obj, filter_fields_lambda, filter_values_lambda,
#                                                convert_fields_lambda, convert_values_lambda,
#                                                 skip_blanks, enable_field, convert_to_js)
#
#
# def get_fields_and_values_from_instance(instance, filter_fields_lambda=None, filter_values_lambda=None,
#                                         convert_fields_lambda = None, convert_values_lambda = None,
#                                         skip_blanks=True, enable_field=None, convert_to_js= True):
#
#     if enable_field != None:
#         if not getattr(instance, enable_field) :
#             return None
#
#     settings_dict = model_to_dict(instance)
#
#     # Remove blank values
#     if skip_blanks:
#         settings_dict = {f: v for f, v in settings_dict.items() if v is not None and v != ""}
#
#     # Filter settings if provided
#     if filter_fields_lambda:
#         settings_dict = {f: v for f, v in settings_dict.items() if filter_fields_lambda(f)}
#
#     if filter_values_lambda:
#         settings_dict = {f: v for f, v in settings_dict.items() if filter_values_lambda(v)}
#
#     if convert_fields_lambda:
#         settings_dict = { convert_fields_lambda(f): v for f, v in settings_dict.items()}
#
#     if convert_values_lambda:
#         settings_dict = { f: convert_values_lambda(v) for f, v in settings_dict.items()}
#
#     if convert_to_js:
#         # Wrap string values in ""
#         settings_dict.update({f: str('"' + v + '"') for f, v in settings_dict.items() if isinstance(v, string_types)})
#         # Convert Bool values to javascript lowercase
#         settings_dict.update({f: str(v).lower() for f, v in settings_dict.items() if isinstance(v, bool)})
#
#     return settings_dict

