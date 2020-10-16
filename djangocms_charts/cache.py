from django.conf import settings
from django.core.cache import cache, InvalidCacheBackendError
from django.core.cache import caches
from cms_named_menus.settings import CACHE_DURATION


KEY_PREFIX = 'djangocms_charts_'


def get_charts_cache():
    djangocms_charts_cache = getattr(settings, 'DJANGOCMS_CHARTS_CACHE', None)
    if djangocms_charts_cache:
        try:
            charts_cache = caches[djangocms_charts_cache]
            if charts_cache is cache:
                raise Exception('DjangoCMS Charts - Do not assign charts to the DEFAULT CACHE')
            return charts_cache
        except InvalidCacheBackendError:
            return None


charts_cache = get_charts_cache()


def _key(kls, id):
    return '{prefix}_{kls}_{id}'.format(prefix=KEY_PREFIX, kls=kls, id=id)


def get(kls, id):
    if charts_cache:
        key = _key(kls, id)
        return charts_cache.get(key, None)


def set(kls, id, inst):  # @ReservedAssignment
    if charts_cache:
        key = _key(kls, id)
        charts_cache.set(key, inst, CACHE_DURATION)


def delete(kls, id):
    if charts_cache:
        delete_many(kls, [id])


def delete_many(kls, ids):
    if charts_cache:
        keys = [_key(kls, id) for id in ids]
        charts_cache.delete_many(keys)


def clear_all():
    if charts_cache:
        charts_cache.clear()
