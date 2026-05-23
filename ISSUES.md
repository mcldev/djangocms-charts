# djangocms-charts — Code Issues & Recommended Fixes

Scope: a static review of `djangocms-charts` 3.1.0 against its declared
target stack — Django **4.2 LTS**, django CMS **3.11**, django-select2
**>=8.0**, Python **3.9 – 3.11**. **No version upgrades are proposed**;
all fixes below are intended to work within the current declared spec.

Severity legend:
- 🔴 **Bug** — broken functionality, crashes, or data loss
- 🟠 **Latent bug** — works on the happy path, breaks on edge cases
- 🟡 **Code smell / maintenance** — works today, but fragile or unclear
- 🔵 **Cleanup** — dead code, typos, unused imports

---

## 1. Critical bugs (likely break at runtime)

### 1.1 ✅ ~~`views.py` imports a removed django-cms function~~ — **RESOLVED**
~~`djangocms_charts/views.py:2`~~
~~`from cms.utils.moderator import get_cmsplugin_queryset`~~

Fixed in branch `fix/2026-05-23_chart-as-json`: the bad import was removed and
replaced with the public API — `from cms.models import CMSPlugin` with
`CMSPlugin.objects.filter(parent_id=chart_id)`.

### 1.2 ✅ ~~`views.py` returns `Http404` instead of raising it~~ — **RESOLVED**
~~`djangocms_charts/views.py:29`~~

Fixed in branch `fix/2026-05-23_chart-as-json`: `return Http404(...)` is now
`raise Http404(...)`.

### 1.3 🔴 `ForeignKey(on_delete=CASCADE)` cascades into chart/dataset rows
`djangocms_charts/models.py:48` and `djangocms_charts/models_datasets.py:33-36`
```python
chart_options_group = models.ForeignKey(ChartOptionsGroupModel,
    on_delete=models.CASCADE, ..., blank=True, null=True)
colors             = models.ForeignKey('ColorGroupModel',
    on_delete=models.CASCADE, ..., blank=True, null=True)
dataset_options_group = models.ForeignKey('DatasetOptionsGroupModel',
    on_delete=models.CASCADE, ..., blank=True, null=True)
xAxis              = models.ForeignKey('AxisOptionsGroupModel',
    on_delete=models.CASCADE, ..., blank=True, null=True)
yAxis              = models.ForeignKey('AxisOptionsGroupModel',
    on_delete=models.CASCADE, ..., blank=True, null=True)
```
Every chart and dataset references *reusable*, nullable lookup objects
with `CASCADE`. **Deleting a single color group, axis, or options group
removes every chart and dataset that referenced it.** That is almost
certainly not the intended semantics for nullable "preset" relations.

**Fix** — change all five to `on_delete=models.SET_NULL` and add a
migration. (Pure Django field-attribute migration, no data change.)

### 1.4 ✅ ~~`clean_table_data` returns `None` for empty input~~ — **RESOLVED**

Fixed: `clean_table_data` now returns `'[]'` on the empty branch so the
follow-up `clean()` receives JSON-parseable input and raises a proper
`ValidationError` instead of a 500 `TypeError`.

### 1.5 ✅ ~~Both form `clean()` methods drop the return value~~ — **RESOLVED**

Fixed: `return cleaned_data` added to the end of both
`OptionsInlineFormBase.clean()` and `DatasetInputForm.clean()`.
`DatasetInputForm.clean()` also now uses `or '[]'` guard so a missing
`table_data` key never reaches `json.loads(None)`.

### 1.6 ✅ ~~`get_chart_width()` / `get_chart_height()` crash when the field is blank~~ — **RESOLVED**

Fixed: both methods now guard with `if not self.chart_width: return ''`
(and equivalent for `chart_height`) before calling `.isnumeric()`.

### 1.7 ✅ ~~`ColorInputForm.__init__` raises `KeyError` for color rows without `types`/`labels`~~ — **RESOLVED**

Fixed: `self.initial['types']` / `self.initial['labels']` replaced with
`self.initial.get('types')` / `self.initial.get('labels')`.

---

## 2. Multi-site correctness

### 2.1 🟠 `ChartJsPlugin.render` ignores the current request's site
`djangocms_charts/cms_plugins.py:54-55`
```python
global_options_list = GlobalOptionsGroupModel.get_global_options()
chart_data = instance.get_chart_as_dict()
```
Both calls fall back to `settings.SITE_ID` instead of using the request's
current site. On any multi-site install with the sites framework, every
site renders Site #1's global options/colors.

**Fix** — pass the resolved site id through:
```python
from django.contrib.sites.shortcuts import get_current_site
site_id = get_current_site(context['request']).id
global_options_list = GlobalOptionsGroupModel.get_global_options(site_id)
chart_data = instance.get_chart_as_dict(site_id=site_id)
```

### 2.2 🟡 Cache keys for global options are not site-scoped distinctly enough
`djangocms_charts/models_options.py:147-181`
The key is `{class_name}_options_{site_id}` and `{class_name}_colors_{site_id}` —
fine in itself, but `clear_all()` (called from many `save()` paths)
clears the entire cache backend, which evicts every site's globals on
every chart edit. Document this trade-off or switch to targeted
`delete_many` using a registry of keys.

---

## 3. Data parsing / dataset bugs

### 3.1 🟠 `_get_datasets_as_coordinate_values` crashes when `labels` is shorter than the row
`djangocms_charts/models_datasets.py:341-368`
```python
if self._has_x_labels:
    labels = self._table_data[0][self._has_data_labels:]
else:
    labels = ['x', 'y', 'r'][:len(self._table_data[0][self._has_data_labels:])]
...
data_list.append({labels[i]: self._table_data[r][i + self._has_data_labels]
                  for i in range(len(labels))})
```
If `labels_top` is True but the user supplies fewer header columns than
data columns, `range(len(labels))` is shorter than the row and silently
drops cells. If the row is shorter than `labels`, `IndexError`.

**Fix** — bound by the *minimum* of the two and validate at form clean
time that all rows have the same width and that coordinate charts have
2 or 3 header columns.

### 3.2 🟠 `_init_data` memoization never refreshes
`djangocms_charts/models_datasets.py:235-252`
```python
def _init_data(self):
    if hasattr(self, '_table_data'):
        return
    ...
```
The cached `_table_data` is tied to the instance. If `table_data` (or
`data_series_format` / `labels_top` / `labels_left`) is reassigned in
the same process, subsequent calls return the stale parse. This is a
trap in tests and in admin save-flows that mutate the instance.

**Fix** — invalidate on field change, or recompute each call (the work
is cheap relative to chart rendering).

### 3.3 🟡 `transpose([])` and ragged rows
`djangocms_charts/utils.py:3-6`
`map(list, zip(*the_array))` silently truncates to the shortest row.
The test `test_transpose_empty` covers `[]`, but ragged input
(`[[1, 2], [3]]`) is silently lossy. Add a form-level validator.

### 3.4 🟡 `apply_colors` is invoked three times per chart
`models.py:120-125` plus `models_datasets.py:321-322`
Each dataset is walked once in `get_datasets()` (own colors), then again
in `get_chart_as_dict()` for chart colors, then a third time for global
colors. `setdefault` makes this idempotent so it isn't wrong, just
wasteful for charts with many datasets — collapse to a single pass
ordered dataset → chart → global.

---

## 4. Options / JSON coercion

### 4.1 🟠 `OptionsBase.get_json_value` 'json' type mangles strings with apostrophes
`djangocms_charts/models_options.py:51-52`
```python
elif val_type == 'json':
    val = json.loads(val.replace("'", '"'))
```
Single-quote → double-quote replacement is a hack for "Pythonic" JSON
input but corrupts legitimate values like `["O'Brien"]`. Same trick
appears in `ColorModel.get_types`/`get_labels`
(`models_colors.py:15-21`) and in `ColorInputForm.__init__`.

**Fix** — accept strict JSON in the admin (document it) or use `ast.literal_eval`,
which understands Python literals natively, then `json.dumps` the
result.

### 4.2 🟠 'function' type is injected into the page with `|safe`
`djangocms_charts/templates/djangocms_charts/chartjs.html:34-37` and
`templatetags/chart_tags.py:5-7`
The `clean_json` filter strips the `FUNC_START:` / `:FUNC_END` markers,
producing raw JavaScript that's pasted into the page with `|safe`.
Anyone with admin access to edit chart options can execute arbitrary JS
in the context of authenticated viewers. Reachable only by admins,
which is the documented contract, but it should be called out.

**Mitigations:**
- Restrict the `function` option type behind a feature flag
  (`DJANGOCMS_CHARTS_ALLOW_JS_FUNCTIONS = False` by default).
- Or scope it to superusers only via a form-level check in the inline
  forms.

### 4.3 🟡 `boolean` coercion is asymmetric for negative ints
`djangocms_charts/models_options.py:46-50`
`'-1'.isnumeric()` is False, so the value falls through to the string
check and becomes `False`. Most users won't notice, but `0`/`-0`/`1`
behave differently from `-1`. Use:
```python
try:
    val = bool(int(val))
except ValueError:
    val = val.strip().lower() == 'true'
```

### 4.4 🟡 `Http404` rather than `JsonResponse` for disabled globals
`djangocms_charts/views.py:27-32` — the JSON endpoint returns/raises
HTML 404 for an existing but disabled options group. Consumers asking
for JSON would expect `JsonResponse({'error': ...}, status=404)`.

---

## 5. Cache layer

### 5.1 🟡 `cache.py` shadows the builtin `set`
`djangocms_charts/cache.py:36`
The `# @ReservedAssignment` comment shows the author was aware, but
within the module `set(...)` is now both the builtin and the cache
function. Rename to `set_value`/`store` and update the two call sites
(`models.py:177`, `models_options.py:160, 180`).

### 5.2 🟡 `is` identity check on cache backends
`djangocms_charts/cache.py:16`
```python
if charts_cache is cache:
```
The proxy `cache` may not be identical to a value pulled from `caches[name]`
even when both point at the same backend. Compare configuration
dictionaries or, better, check the `name` against `'default'`.

### 5.3 🟡 `clear_all()` evicts unrelated keys from the chart cache
Acceptable for a *dedicated* cache (as the README warns), but the
warning is a `warnings.warn` at import time which Django normally
suppresses in production. Make this a hard error during system check,
e.g. via a `django.core.checks.register` callback.

---

## 6. Migrations / model definitions

### 6.1 🟠 `AxisOptionsGroupModel.save` clears the cache twice on first save
`djangocms_charts/models_axes.py:81-85`
```python
def save(self, *args, **kwargs):
    super().save(*args, **kwargs)         # OptionsGroupBase.save → clear_all()
    self.slug = slugify(f'{self.id}_{self.name}')
    super().save(update_fields=['slug'])   # OptionsGroupBase.save → clear_all() again
    charts_cache.clear_all()               # …and once more here, explicitly
```
At minimum the explicit `charts_cache.clear_all()` is redundant. The
second `super().save()` could also bypass the override by calling
`models.Model.save(self, update_fields=['slug'])` to suppress the
duplicate invalidation.

### 6.2 🟡 `xAxis` / `yAxis` field names violate PEP 8
`djangocms_charts/models_datasets.py:35-36`
Camel-case attribute names propagate everywhere — `chart.xAxis`,
`other_dataset.xAxis.get_axis_id('x')`. Renaming requires a migration,
so this is informational rather than urgent.

### 6.3 🟡 `migrations/0011_alter_chartmodel_cmsplugin_ptr_and_more.py` depends on `cms 0022_auto_20180620_1551`
That migration is ancient but still present in django CMS 3.11. Works,
but every fresh chart migration should depend on the *latest* cms
migration to ensure ordering — confirm with `python -m django makemigrations --dry-run`.

### 6.4 🔵 `migrations/0006_migrate_old_chart_data.py` and `0007/0008/0009`
Data migrations from the 2.x → 3.0 refactor are still in the migration
graph. They are no-ops on fresh databases (the old tables don't exist),
but the chained `try/except` ladder in `migration_utils.py:148-160` is
hard to follow. Acceptable to keep for upgrade paths; consider gating
behind a `DJANGOCMS_CHARTS_RUN_LEGACY_MIGRATIONS` setting and otherwise
short-circuiting.

---

## 7. Plugin / admin

### 7.1 🔵 Typo in plugin fieldset label
`djangocms_charts/cms_plugins.py:94`
```python
(_("Datasetl Options"), { ... })   # should be "Dataset Options"
```

### 7.2 🔵 Unused import in `admin.py`
`djangocms_charts/admin.py:1`
```python
from adminsortable2.admin import SortableInlineAdminMixin
```
Never used. Remove the import (and the unused `django-admin-sortable2`
test dependency in `setup.py:46` if no other code paths need it).

### 7.3 🔵 `default_app_config` is a no-op on Django 4.2
`djangocms_charts/__init__.py:1`
```python
default_app_config = 'djangocms_charts.apps.ChartsConfig'
```
Django auto-discovers a single `AppConfig` in `apps.py`, and the
attribute is ignored from Django 4.1+. Safe to delete the line.

### 7.4 🔵 `templates/temp_js_code.txt` is malformed
The file is a stray scratch pad for the `get_keys` introspection
helper, but its braces are mismatched (every block `{` is written as
`}`). It is not loaded by any template/JS. Delete or move outside
`templates/` so package consumers don't see it.

### 7.5 🟡 Old front-end assets bundled
`djangocms_charts/widgets.py:11-24` references `handsontable.full.js`,
`jquery.contextMenu.js`, `jquery-ui.position.js`, `json2.js`, and
`bootstrap3-typeahead.js`. None are loaded from a CDN; they live in
`static/`. They still work but no longer receive security fixes. If
the project is happy to stay on these versions, document the deliberate
pinning in the README so future maintainers don't churn on them.

### 7.6 🟡 `forms.py` bundles `jquery-3.5.1.min.js`
`djangocms_charts/forms.py:35` — jQuery 3.5.1 has known low-severity
CVEs (XSS in `.html()` for crafted markup). Admin-only surface, but
swap for whatever jQuery is already pulled in by django CMS admin
instead of bundling a second copy.

### 7.7 🟡 `widgets.py` `render_additions` crashes when no language is active
`djangocms_charts/widgets.py:30`
```python
language = get_language().split('-')[0]
```
`get_language()` can return `None` in scripts/management commands. Add
a fallback:
```python
language = (get_language() or 'en').split('-')[0]
```

---

## 8. Dead code

| Location | Notes |
|---|---|
| `djangocms_charts/utils.py:15-16` | `color_variants` is exported but unused. |
| `djangocms_charts/migration_utils.py:34-35` | `update_indexes` is unused. |
| `djangocms_charts/migration_utils.py:43-90` | `copy_old_table_to_model` only used by legacy migrations — keep if upgrade paths still matter, otherwise delete. |
| `tests/test_charts.py:19` | `OptionsBase` imported but never used. |
| `tests/test_charts.py:9-14` | `RequestFactory`, `override_settings`, `create_page` are imported but unused. |
| `djangocms_charts/cms_plugins.py:5` | `json` is used; `settings` is used; OK. |

---

## 9. Suggested commit order

Each block stands alone — merge in this order to avoid noisy diffs:

1. **§1.1, §1.2** Fix `views.py` (broken imports / `return Http404`).
2. **§1.3** Migration: `CASCADE` → `SET_NULL` on the five FKs.
3. **§1.4, §1.5, §1.6, §1.7** Form/model crash guards.
4. **§2.1** Pass `site_id` through `render`.
5. **§3.1, §3.2** Dataset parsing edge cases + memoization.
6. **§4.1, §4.3, §4.4** Options coercion polish.
7. **§5.1, §5.2** Cache module rename + identity check.
8. **§6.1, §7.1, §7.2, §7.3, §7.4** Small cleanups.
9. **§4.2, §7.5, §7.6** Security/asset hygiene (opt-in flags).

Tests already cover the dataset / options / colors / axes paths so most
of these fixes can be verified with:

```bash
pip install -e ".[test]"
python -m django test tests --settings=tests.settings -v 2
```

Add regression tests for §1.1 (URL include), §1.4 (empty table data),
§1.6 (blank width/height), §1.7 (color inline with no `types`/`labels`),
and §3.1 (coordinate parse mismatch) when fixing each.
