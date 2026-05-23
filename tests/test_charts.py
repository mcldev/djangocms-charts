"""
Unit tests for djangocms-charts.
Verifies models, utils, options, datasets, colors, axes, and CMS plugin registration
work correctly with Django 4.2, djangoCMS 3.11, and Python 3.11.
"""
import json

from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory, override_settings

from cms.api import add_plugin, create_page
from cms.models import Placeholder
from cms.plugin_pool import plugin_pool
from cms.test_utils.testcases import CMSTestCase

from djangocms_charts.consts import CHART_TYPES
from djangocms_charts.forms import DatasetInputForm, OptionsInlineFormBase
from djangocms_charts.models import ChartModel, DatasetModel
from djangocms_charts.models_options import (
    OptionsBase,
    ChartOptionsGroupModel,
    ChartOptionsModel,
    DatasetOptionsGroupModel,
    DatasetOptionsModel,
    GlobalOptionsGroupModel,
    GlobalOptionsModel,
    ChartSpecificOptionsModel,
)
from djangocms_charts.models_axes import AxisOptionsGroupModel, AxisOptionsModel
from djangocms_charts.models_colors import ColorGroupModel, ColorModel
from djangocms_charts.utils import transpose, get_unique_list, color_variant


# ============================================================
# Utility Tests
# ============================================================

class TransposeTests(TestCase):
    """Test the transpose() utility function."""

    def test_transpose_square(self):
        data = [[1, 2], [3, 4]]
        self.assertEqual(transpose(data), [[1, 3], [2, 4]])

    def test_transpose_rectangular(self):
        data = [['a', 'b', 'c'], ['d', 'e', 'f']]
        result = transpose(data)
        self.assertEqual(result, [['a', 'd'], ['b', 'e'], ['c', 'f']])

    def test_transpose_single_row(self):
        data = [[1, 2, 3]]
        self.assertEqual(transpose(data), [[1], [2], [3]])

    def test_transpose_empty(self):
        self.assertEqual(transpose([]), [])

    def test_transpose_roundtrip(self):
        data = [['x', 'y'], ['1', '2'], ['3', '4']]
        self.assertEqual(transpose(transpose(data)), data)


class GetUniqueListTests(TestCase):
    """Test the get_unique_list() utility function."""

    def test_removes_duplicates(self):
        items = [{'id': 1, 'v': 'a'}, {'id': 2, 'v': 'b'}, {'id': 1, 'v': 'c'}]
        result = get_unique_list(items)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[1]['id'], 2)

    def test_empty_list(self):
        self.assertEqual(get_unique_list([]), [])

    def test_filters_none(self):
        items = [None, {'id': 1}, None, {'id': 2}]
        result = get_unique_list(items)
        self.assertEqual(len(result), 2)

    def test_custom_key(self):
        items = [{'name': 'a', 'x': 1}, {'name': 'b', 'x': 2}, {'name': 'a', 'x': 3}]
        result = get_unique_list(items, key='name')
        self.assertEqual(len(result), 2)


class ColorVariantTests(TestCase):
    """Test the color_variant() utility function."""

    def test_lighten(self):
        result = color_variant('#000000', 10)
        self.assertEqual(result, '#0a0a0a')

    def test_darken(self):
        result = color_variant('#ffffff', -10)
        self.assertEqual(result, '#f5f5f5')

    def test_no_change(self):
        result = color_variant('#808080', 0)
        self.assertEqual(result, '#808080')

    def test_clamp_high(self):
        result = color_variant('#fafafa', 100)
        self.assertEqual(result, '#ffffff')

    def test_clamp_low(self):
        result = color_variant('#050505', -100)
        self.assertEqual(result, '#000000')

    def test_invalid_format_raises(self):
        with self.assertRaises(Exception):
            color_variant('red', 10)


# ============================================================
# Chart Type Constants Tests
# ============================================================

class ChartTypesTests(TestCase):
    """Test CHART_TYPES enum and helpers."""

    def test_coordinate_types(self):
        self.assertTrue(CHART_TYPES.is_coordinate_type(CHART_TYPES.SCATTER))
        self.assertTrue(CHART_TYPES.is_coordinate_type(CHART_TYPES.BUBBLE))
        self.assertTrue(CHART_TYPES.is_coordinate_type(CHART_TYPES.LINE_XY))

    def test_non_coordinate_types(self):
        self.assertFalse(CHART_TYPES.is_coordinate_type(CHART_TYPES.LINE))
        self.assertFalse(CHART_TYPES.is_coordinate_type(CHART_TYPES.BAR))
        self.assertFalse(CHART_TYPES.is_coordinate_type(CHART_TYPES.PIE))
        self.assertFalse(CHART_TYPES.is_coordinate_type(CHART_TYPES.DOUGHNUT))
        self.assertFalse(CHART_TYPES.is_coordinate_type(CHART_TYPES.RADAR))
        self.assertFalse(CHART_TYPES.is_coordinate_type(CHART_TYPES.POLAR))

    def test_get_choices_contains_all(self):
        choice_values = [c[0] for c in CHART_TYPES.get_choices]
        self.assertIn('line', choice_values)
        self.assertIn('bar', choice_values)
        self.assertIn('pie', choice_values)
        self.assertIn('scatter', choice_values)
        self.assertIn('bubble', choice_values)
        self.assertEqual(len(choice_values), 10)


# ============================================================
# Options System Tests
# ============================================================

class OptionsBaseTests(TestCase):
    """Test OptionsBase.get_json_value() type coercion."""

    def _make_option(self):
        """Helper: returns a ChartOptionsModel without saving."""
        group = ChartOptionsGroupModel.objects.create(name='test_group')
        return ChartOptionsModel(options_group=group, label='test', type='text', value='hello')

    def test_text_value(self):
        opt = self._make_option()
        opt.type = 'text'
        opt.value = '  hello  '
        self.assertEqual(json.loads(opt.get_json_value()), 'hello')

    def test_number_int(self):
        opt = self._make_option()
        opt.type = 'number'
        opt.value = '42'
        self.assertEqual(json.loads(opt.get_json_value()), 42)

    def test_number_float(self):
        opt = self._make_option()
        opt.type = 'number'
        opt.value = '3.14'
        self.assertAlmostEqual(json.loads(opt.get_json_value()), 3.14)

    def test_boolean_true(self):
        opt = self._make_option()
        opt.type = 'boolean'
        opt.value = 'true'
        self.assertEqual(json.loads(opt.get_json_value()), True)

    def test_boolean_false(self):
        opt = self._make_option()
        opt.type = 'boolean'
        opt.value = 'false'
        self.assertEqual(json.loads(opt.get_json_value()), False)

    def test_boolean_numeric(self):
        opt = self._make_option()
        opt.type = 'boolean'
        opt.value = '1'
        self.assertEqual(json.loads(opt.get_json_value()), True)
        opt.value = '0'
        self.assertEqual(json.loads(opt.get_json_value()), False)

    def test_json_value(self):
        opt = self._make_option()
        opt.type = 'json'
        opt.value = '{"key": "val"}'
        result = json.loads(opt.get_json_value())
        self.assertEqual(result, {"key": "val"})

    def test_array_comma_separated(self):
        opt = self._make_option()
        opt.type = 'array'
        opt.value = 'a,b,c'
        result = json.loads(opt.get_json_value())
        self.assertEqual(result, ['a', 'b', 'c'])

    def test_array_newline_separated(self):
        opt = self._make_option()
        opt.type = 'array'
        opt.value = 'x\ny\nz'
        result = json.loads(opt.get_json_value())
        self.assertEqual(result, ['x', 'y', 'z'])

    def test_function_value(self):
        opt = self._make_option()
        opt.type = 'function'
        opt.value = 'function(x) { return x; }'
        result = json.loads(opt.get_json_value())
        self.assertIn('FUNC_START:', result)
        self.assertIn(':FUNC_END', result)


class OptionsGroupTests(TestCase):
    """Test options group dict building with dot-separated labels."""

    def test_nested_options_dict(self):
        group = ChartOptionsGroupModel.objects.create(name='test_nested')
        ChartOptionsModel.objects.create(
            options_group=group, label='options.hover.mode', type='text', value='nearest')
        ChartOptionsModel.objects.create(
            options_group=group, label='options.hover.intersect', type='boolean', value='false')

        result = group.get_as_dict()
        self.assertEqual(result['options']['hover']['mode'], 'nearest')
        self.assertEqual(result['options']['hover']['intersect'], False)

    def test_flat_option(self):
        group = ChartOptionsGroupModel.objects.create(name='test_flat')
        ChartOptionsModel.objects.create(
            options_group=group, label='responsive', type='boolean', value='true')

        result = group.get_as_dict()
        self.assertEqual(result['responsive'], True)


# ============================================================
# Color System Tests
# ============================================================

class ColorModelTests(TestCase):
    """Test color model parsing."""

    def test_get_colors_splits(self):
        group = ColorGroupModel.objects.create(name='palette')
        color = ColorModel.objects.create(
            color_group=group,
            types="['line', 'bar']",
            labels="['backgroundColor']",
            colors='#ff0000,#00ff00,#0000ff'
        )
        self.assertEqual(color.get_colors(), ['#ff0000', '#00ff00', '#0000ff'])

    def test_get_types_parses_json(self):
        group = ColorGroupModel.objects.create(name='palette2')
        color = ColorModel.objects.create(
            color_group=group,
            types="['line']",
            labels="['borderColor']",
            colors='#abc'
        )
        self.assertEqual(color.get_types(), ['line'])

    def test_get_labels_parses_json(self):
        group = ColorGroupModel.objects.create(name='palette3')
        color = ColorModel.objects.create(
            color_group=group,
            types="['bar']",
            labels="['backgroundColor', 'borderColor']",
            colors='#abc'
        )
        self.assertEqual(color.get_labels(), ['backgroundColor', 'borderColor'])

    def test_color_group_as_dict(self):
        group = ColorGroupModel.objects.create(name='full_palette')
        ColorModel.objects.create(
            color_group=group,
            types="['line']",
            labels="['backgroundColor']",
            colors='#ff0000,#00ff00'
        )
        result = group.get_as_dict()
        self.assertIn('line', result)
        self.assertIn('backgroundColor', result['line'])
        self.assertEqual(result['line']['backgroundColor'], ['#ff0000', '#00ff00'])


# ============================================================
# Axis Model Tests
# ============================================================

class AxisModelTests(TestCase):
    """Test axis option group model."""

    def test_axis_as_dict(self):
        axis = AxisOptionsGroupModel.objects.create(
            name='Left Y', type='linear', display='true', weight=1)
        result = axis.get_axis_as_dict('y')
        self.assertEqual(result['type'], 'linear')
        self.assertEqual(result['display'], True)
        self.assertEqual(result['weight'], 1)
        self.assertIn('y_', result['id'])

    def test_axis_id_format(self):
        axis = AxisOptionsGroupModel.objects.create(name='Bottom X', type='category')
        axis_id = axis.get_axis_id('x')
        self.assertTrue(axis_id.startswith('x_'))

    def test_axis_with_options(self):
        axis = AxisOptionsGroupModel.objects.create(name='WithOpts', type='linear')
        AxisOptionsModel.objects.create(
            options_group=axis, label='ticks.beginAtZero', type='boolean', value='true')
        result = axis.get_axis_as_dict('y')
        self.assertEqual(result['ticks']['beginAtZero'], True)

    def test_axis_str_with_type(self):
        axis = AxisOptionsGroupModel.objects.create(name='TestAxis', type='linear')
        self.assertIn('[linear]', str(axis))

    def test_axis_str_without_type(self):
        axis = AxisOptionsGroupModel.objects.create(name='NoType')
        self.assertNotIn('[', str(axis))


# ============================================================
# Dataset Parsing Tests (using ChartModel as concrete DatasetBase)
# ============================================================

class DatasetBaseTests(CMSTestCase):
    """Test DatasetBase mixin functionality via ChartModel."""

    def _create_chart(self, table_data, chart_type='line',
                      labels_top=True, labels_left=True,
                      data_series_format='rows'):
        placeholder = Placeholder.objects.create(slot='test')
        return add_plugin(placeholder, 'ChartJsPlugin', 'en',
                          label='Test Chart',
                          type=chart_type,
                          table_data=json.dumps(table_data),
                          labels_top=labels_top,
                          labels_left=labels_left,
                          data_series_format=data_series_format)

    def test_get_x_labels_from_rows(self):
        """With data_series_format='rows', labels_top=True, labels_left=True:
        First row = x-labels, first column = dataset names."""
        table_data = [
            ['', 'Jan', 'Feb', 'Mar'],
            ['Sales', '10', '20', '30'],
            ['Returns', '5', '8', '12'],
        ]
        chart = self._create_chart(table_data, data_series_format='rows')
        labels = chart.get_x_labels()
        self.assertEqual(labels, ['Jan', 'Feb', 'Mar'])

    def test_get_datasets_labels_values(self):
        """Test standard label+value dataset extraction."""
        table_data = [
            ['', 'Jan', 'Feb'],
            ['Sales', '10', '20'],
            ['Returns', '5', '8'],
        ]
        chart = self._create_chart(table_data, data_series_format='rows')
        datasets = chart.get_datasets()
        self.assertEqual(len(datasets), 2)
        self.assertEqual(datasets[0]['label'], 'Sales')
        self.assertEqual(datasets[0]['data'], ['10', '20'])
        self.assertEqual(datasets[1]['label'], 'Returns')

    def test_get_datasets_columns_format(self):
        """Test column-oriented data is transposed correctly."""
        table_data = [
            ['', 'Sales', 'Returns'],
            ['Jan', '10', '5'],
            ['Feb', '20', '8'],
        ]
        chart = self._create_chart(table_data, data_series_format='cols')
        datasets = chart.get_datasets()
        self.assertEqual(len(datasets), 2)
        self.assertEqual(datasets[0]['label'], 'Sales')
        self.assertEqual(datasets[0]['data'], ['10', '20'])

    def test_no_labels(self):
        """Test with labels_top=False and labels_left=False."""
        table_data = [
            ['10', '20', '30'],
            ['5', '8', '12'],
        ]
        chart = self._create_chart(table_data, labels_top=False, labels_left=False)
        labels = chart.get_x_labels()
        self.assertEqual(labels, [])
        datasets = chart.get_datasets()
        self.assertEqual(len(datasets), 2)
        self.assertEqual(datasets[0]['data'], ['10', '20', '30'])

    def test_scatter_coordinate_datasets(self):
        """Test scatter chart produces coordinate dicts."""
        table_data = [
            ['x', 'y'],
            ['1', '2'],
            ['3', '4'],
        ]
        chart = self._create_chart(table_data, chart_type='scatter',
                                   labels_top=True, labels_left=False)
        datasets = chart.get_datasets()
        self.assertEqual(len(datasets), 1)
        self.assertEqual(datasets[0]['data'][0], {'x': '1', 'y': '2'})
        self.assertEqual(datasets[0]['data'][1], {'x': '3', 'y': '4'})

    def test_empty_table_data(self):
        """Test with empty table data."""
        chart = self._create_chart([], labels_top=False, labels_left=False)
        self.assertEqual(chart.get_datasets(), [])
        self.assertEqual(chart.get_x_labels(), [])

    def test_coordinate_types_no_x_labels(self):
        """Coordinate types should return empty x_labels."""
        table_data = [
            ['x', 'y'],
            ['1', '2'],
        ]
        chart = self._create_chart(table_data, chart_type='scatter',
                                   labels_top=True, labels_left=False)
        self.assertEqual(chart.get_x_labels(), [])


# ============================================================
# Chart Model Property Tests
# ============================================================

class ChartModelPropertyTests(CMSTestCase):
    """Test ChartModel properties and helpers."""

    def _create_chart(self, **kwargs):
        placeholder = Placeholder.objects.create(slot='test')
        defaults = dict(
            label='My Chart',
            type='bar',
            table_data='[]',
            labels_top=True,
            labels_left=True,
            data_series_format='rows',
        )
        defaults.update(kwargs)
        return add_plugin(placeholder, 'ChartJsPlugin', 'en', **defaults)

    def test_chart_name_slugified(self):
        chart = self._create_chart(label='My Test Chart')
        self.assertEqual(chart.chart_name, 'bar_my-test-chart')

    def test_chart_id(self):
        chart = self._create_chart()
        self.assertTrue(chart.chart_id().startswith('chart_'))

    def test_chart_container_id(self):
        chart = self._create_chart()
        self.assertTrue(chart.chart_container_id().startswith('chart-container_'))

    def test_str_returns_chart_name(self):
        chart = self._create_chart(label='StrTest')
        self.assertEqual(str(chart), chart.chart_name)

    def test_chart_width_numeric(self):
        chart = self._create_chart(chart_width='400')
        self.assertEqual(chart.get_chart_width(), '400px')

    def test_chart_width_css(self):
        chart = self._create_chart(chart_width='50%')
        self.assertEqual(chart.get_chart_width(), '50%')

    def test_chart_height_numeric(self):
        chart = self._create_chart(chart_height='300')
        self.assertEqual(chart.get_chart_height(), '300px')


# ============================================================
# Chart Dict Generation Tests
# ============================================================

class ChartDictTests(CMSTestCase):
    """Test get_chart_as_dict() output structure."""

    def _create_chart_with_data(self):
        placeholder = Placeholder.objects.create(slot='test')
        table_data = [
            ['', 'Jan', 'Feb', 'Mar'],
            ['Revenue', '100', '200', '300'],
        ]
        return add_plugin(placeholder, 'ChartJsPlugin', 'en',
                          label='Revenue Chart',
                          type='bar',
                          table_data=json.dumps(table_data),
                          labels_top=True,
                          labels_left=True,
                          data_series_format='rows',
                          display_title=True,
                          display_legend=True,
                          legend_position='top')

    def test_chart_dict_has_type(self):
        chart = self._create_chart_with_data()
        result = chart.get_chart_as_dict()
        self.assertEqual(result['type'], 'bar')

    def test_chart_dict_has_data(self):
        chart = self._create_chart_with_data()
        result = chart.get_chart_as_dict()
        self.assertIn('data', result)
        self.assertIn('datasets', result['data'])
        self.assertIn('labels', result['data'])

    def test_chart_dict_labels(self):
        chart = self._create_chart_with_data()
        result = chart.get_chart_as_dict()
        self.assertEqual(result['data']['labels'], ['Jan', 'Feb', 'Mar'])

    def test_chart_dict_dataset_values(self):
        chart = self._create_chart_with_data()
        result = chart.get_chart_as_dict()
        ds = result['data']['datasets'][0]
        self.assertEqual(ds['data'], ['100', '200', '300'])
        self.assertEqual(ds['label'], 'Revenue')

    def test_chart_dict_title(self):
        chart = self._create_chart_with_data()
        result = chart.get_chart_as_dict()
        self.assertEqual(result['options']['title']['text'], 'Revenue Chart')
        self.assertTrue(result['options']['title']['display'])

    def test_chart_dict_legend(self):
        chart = self._create_chart_with_data()
        result = chart.get_chart_as_dict()
        self.assertTrue(result['options']['legend']['display'])
        self.assertEqual(result['options']['legend']['position'], 'top')


# ============================================================
# CMS Plugin Registration Tests
# ============================================================

class PluginRegistrationTests(TestCase):
    """Verify plugins are registered with django CMS plugin pool."""

    def test_chartjs_plugin_registered(self):
        self.assertIn('ChartJsPlugin', plugin_pool.plugins)

    def test_dataset_plugin_registered(self):
        self.assertIn('DatasetPlugin', plugin_pool.plugins)

    def test_chartjs_plugin_allows_children(self):
        plugin_cls = plugin_pool.plugins['ChartJsPlugin']
        self.assertTrue(plugin_cls.allow_children)
        self.assertIn('DatasetPlugin', plugin_cls.child_classes)

    def test_dataset_plugin_requires_parent(self):
        plugin_cls = plugin_pool.plugins['DatasetPlugin']
        self.assertTrue(plugin_cls.require_parent)
        self.assertIn('ChartJsPlugin', plugin_cls.parent_classes)


# ============================================================
# Global Options Tests
# ============================================================

class GlobalOptionsTests(TestCase):
    """Test GlobalOptionsGroupModel class methods."""

    def setUp(self):
        self.site = Site.objects.get_current()

    def test_get_global_options_none_when_empty(self):
        result = GlobalOptionsGroupModel.get_global_options(self.site.id)
        self.assertIsNone(result)

    def test_get_global_options_returns_list(self):
        group = GlobalOptionsGroupModel.objects.create(
            name='Global', enabled=True, site=self.site)
        GlobalOptionsModel.objects.create(
            options_group=group, label='responsive', type='boolean', value='true')
        result = GlobalOptionsGroupModel.get_global_options(self.site.id)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 'responsive')

    def test_disabled_global_options_not_returned(self):
        group = GlobalOptionsGroupModel.objects.create(
            name='Disabled', enabled=False, site=self.site)
        GlobalOptionsModel.objects.create(
            options_group=group, label='test', type='text', value='val')
        result = GlobalOptionsGroupModel.get_global_options(self.site.id)
        self.assertIsNone(result)

    def test_get_global_colors_none_when_empty(self):
        result = GlobalOptionsGroupModel.get_global_colors(self.site.id)
        self.assertIsNone(result)

    def test_get_global_colors_returns_dict(self):
        color_group = ColorGroupModel.objects.create(name='global_colors')
        ColorModel.objects.create(
            color_group=color_group,
            types="['bar']",
            labels="['backgroundColor']",
            colors='#ff0000'
        )
        group = GlobalOptionsGroupModel.objects.create(
            name='WithColors', enabled=True, site=self.site, colors=color_group)
        result = GlobalOptionsGroupModel.get_global_colors(self.site.id)
        self.assertIsNotNone(result)
        self.assertIn('bar', result)


# ============================================================
# Issue 1.6 — get_chart_width/height crash on None / empty
# ============================================================

class ChartWidthHeightBlankTests(CMSTestCase):

    def _make_chart(self, **kwargs):
        placeholder = Placeholder.objects.create(slot='wh_test')
        defaults = dict(label='W', type='bar', table_data='[]',
                        labels_top=True, labels_left=True, data_series_format='rows')
        defaults.update(kwargs)
        return add_plugin(placeholder, 'ChartJsPlugin', 'en', **defaults)

    def test_chart_width_none_returns_empty_string(self):
        chart = self._make_chart()
        chart.chart_width = None
        self.assertEqual(chart.get_chart_width(), '')

    def test_chart_width_empty_string_returns_empty_string(self):
        chart = self._make_chart()
        chart.chart_width = ''
        self.assertEqual(chart.get_chart_width(), '')

    def test_chart_height_none_returns_empty_string(self):
        chart = self._make_chart()
        chart.chart_height = None
        self.assertEqual(chart.get_chart_height(), '')

    def test_chart_height_empty_string_returns_empty_string(self):
        chart = self._make_chart()
        chart.chart_height = ''
        self.assertEqual(chart.get_chart_height(), '')


# ============================================================
# Issues 1.4 & 1.5 — DatasetInputForm clean methods
# ============================================================

class DatasetFormCleanTests(TestCase):

    def _make_form(self, table_data_value):
        form = DatasetInputForm.__new__(DatasetInputForm)
        form.cleaned_data = {'table_data': table_data_value}
        form._errors = {}
        return form

    def test_clean_table_data_empty_string_does_not_return_none(self):
        """Issue 1.4: implicit None return causes TypeError in clean()."""
        form = self._make_form('')
        result = form.clean_table_data()
        self.assertIsNotNone(result)

    def test_clean_table_data_empty_is_json_parseable(self):
        """Issue 1.4: result must be JSON-parseable so clean() can call json.loads()."""
        form = self._make_form('')
        result = form.clean_table_data()
        self.assertIsNotNone(result)
        json.loads(result)  # must not raise

    def test_clean_table_data_nonempty_returns_valid_json(self):
        form = self._make_form(json.dumps([['', 'Jan', 'Feb'], ['Sales', '10', '20']]))
        result = form.clean_table_data()
        self.assertIsNotNone(result)
        self.assertIsInstance(json.loads(result), list)

    def test_dataset_form_clean_returns_cleaned_data(self):
        """Issue 1.5: clean() must return cleaned_data."""
        form = self._make_form(json.dumps([['', 'Jan'], ['Sales', '10']]))
        result = form.clean()
        self.assertIsNotNone(result)
        self.assertIn('table_data', result)

    def test_dataset_form_clean_raises_validation_error_for_empty_table(self):
        """Issues 1.4+1.5: empty table must raise ValidationError, not TypeError/500."""
        form = self._make_form('')
        form.clean_table_data()  # returns '[]', sets cleaned state
        form.cleaned_data['table_data'] = '[]'
        with self.assertRaises(ValidationError):
            form.clean()


# ============================================================
# Issue 1.5 — OptionsInlineFormBase.clean() missing return
# ============================================================

class OptionsFormCleanTests(TestCase):

    def test_options_inline_clean_returns_cleaned_data(self):
        """Issue 1.5: OptionsInlineFormBase.clean() must return cleaned_data."""
        group = ChartOptionsGroupModel.objects.create(name='options_clean_test')
        instance = ChartOptionsModel(options_group=group, label='x', type='number', value='10')

        form = OptionsInlineFormBase.__new__(OptionsInlineFormBase)
        form.cleaned_data = {'value': '10', 'type': 'number'}
        form._errors = {}
        form.instance = instance
        result = form.clean()
        self.assertIsNotNone(result)
        self.assertEqual(result['value'], '10')


# ============================================================
# Issue 1.7 — ColorInputForm.__init__ KeyError on missing keys
# ============================================================

class ColorInputFormInitTests(TestCase):

    def _bound_form_class(self):
        from django.forms import modelform_factory
        from djangocms_charts.forms import ColorInputForm
        return modelform_factory(ColorModel, form=ColorInputForm,
                                 fields=['types', 'labels', 'colors'])

    def test_initial_without_types_key_does_not_raise_keyerror(self):
        """Issue 1.7: inline row whose initial has the FK but no types/labels must not raise KeyError."""
        BoundForm = self._bound_form_class()
        # Simulate an extra inline row: initial is non-empty (has FK) but has no types/labels
        try:
            BoundForm(initial={'color_group': 1})
        except KeyError as exc:
            self.fail(f'ColorInputForm.__init__ raised KeyError: {exc}')

    def test_initial_with_types_and_labels_is_parsed(self):
        BoundForm = self._bound_form_class()
        form = BoundForm(initial={
            'types': "['bar', 'line']",
            'labels': "['backgroundColor']",
        })
        self.assertEqual(form.initial['types'], ['bar', 'line'])
        self.assertEqual(form.initial['labels'], ['backgroundColor'])


# ============================================================
# Issue 1.3 — FK on_delete=CASCADE destroys charts/datasets
# ============================================================

class ForeignKeyCascadeTests(CMSTestCase):
    """Deleting a reusable preset (options group, color group, axis) must
    nullify the FK on charts/datasets, not delete them."""

    def _make_chart(self, **kwargs):
        placeholder = Placeholder.objects.create(slot='fk_test')
        defaults = dict(label='FK Test', type='bar', table_data='[]',
                        labels_top=True, labels_left=True, data_series_format='rows')
        defaults.update(kwargs)
        return add_plugin(placeholder, 'ChartJsPlugin', 'en', **defaults)

    def test_deleting_chart_options_group_nullifies_fk(self):
        group = ChartOptionsGroupModel.objects.create(name='deletable_chart_opts')
        chart = self._make_chart()
        chart.chart_options_group = group
        chart.save()
        pk = chart.pk

        group.delete()

        self.assertTrue(ChartModel.objects.filter(pk=pk).exists(),
                        'chart was deleted when its chart_options_group was deleted')
        chart.refresh_from_db()
        self.assertIsNone(chart.chart_options_group)

    def test_deleting_color_group_nullifies_fk(self):
        color_group = ColorGroupModel.objects.create(name='deletable_colors')
        chart = self._make_chart()
        chart.colors = color_group
        chart.save()
        pk = chart.pk

        color_group.delete()

        self.assertTrue(ChartModel.objects.filter(pk=pk).exists(),
                        'chart was deleted when its color group was deleted')
        chart.refresh_from_db()
        self.assertIsNone(chart.colors)

    def test_deleting_dataset_options_group_nullifies_fk(self):
        ds_group = DatasetOptionsGroupModel.objects.create(name='deletable_ds_opts')
        chart = self._make_chart()
        chart.dataset_options_group = ds_group
        chart.save()
        pk = chart.pk

        ds_group.delete()

        self.assertTrue(ChartModel.objects.filter(pk=pk).exists(),
                        'chart was deleted when its dataset_options_group was deleted')
        chart.refresh_from_db()
        self.assertIsNone(chart.dataset_options_group)

    def test_deleting_xaxis_nullifies_fk(self):
        axis = AxisOptionsGroupModel.objects.create(name='deletable_x', type='category')
        chart = self._make_chart()
        chart.xAxis = axis
        chart.save()
        pk = chart.pk

        axis.delete()

        self.assertTrue(ChartModel.objects.filter(pk=pk).exists(),
                        'chart was deleted when its xAxis was deleted')
        chart.refresh_from_db()
        self.assertIsNone(chart.xAxis)

    def test_deleting_yaxis_nullifies_fk(self):
        axis = AxisOptionsGroupModel.objects.create(name='deletable_y', type='linear')
        chart = self._make_chart()
        chart.yAxis = axis
        chart.save()
        pk = chart.pk

        axis.delete()

        self.assertTrue(ChartModel.objects.filter(pk=pk).exists(),
                        'chart was deleted when its yAxis was deleted')
        chart.refresh_from_db()
        self.assertIsNone(chart.yAxis)

