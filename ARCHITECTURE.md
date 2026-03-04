# djangocms-charts — Architecture & Module Documentation

## Overview

`djangocms-charts` is a **django CMS plugin** that allows content editors to create and configure **Chart.js** charts directly within the CMS page editor. Charts are defined via table data (pasted or CSV-uploaded), with full support for multiple datasets, custom axes, color groups, and reusable option presets.

## Key Features

- **10 Chart Types**: line, line_xy, bar, horizontalBar, radar, polarArea, pie, doughnut, bubble, scatter
- **Inline Table Editor**: paste or upload CSV data directly in the admin
- **Child Datasets**: a chart plugin can have child dataset plugins for multi-dataset charts
- **Reusable Options Groups**: global, chart-level, dataset-level, and axis options can be saved and reused
- **Color Groups**: define color palettes per chart type and apply globally, per-chart, or per-dataset
- **Caching**: optional dedicated cache backend for chart JSON output
- **Global Options**: site-wide Chart.js defaults (rendered once per page)

## Module Breakdown

### `models.py` — Main Plugin Models
- **`ChartModel`** (`CMSPlugin` + `DatasetBase`): The main chart plugin model. Stores chart-level settings (title, legend, dimensions, CSS classes) and generates the full Chart.js JSON dictionary via `get_chart_as_dict()`.
- **`DatasetModel`** (`CMSPlugin` + `DatasetBase`): A child dataset plugin that can be nested inside a `ChartModel` to add additional data series.

### `models_datasets.py` — Dataset Logic (Mixin)
- **`DatasetBase`** (abstract): Core mixin for both `ChartModel` and `DatasetModel`. Handles:
  - Parsing table data (JSON array of arrays)
  - Transposing rows↔columns based on `data_series_format`
  - Extracting x-axis labels
  - Building dataset dictionaries for label+value types (line/bar/pie/etc.) and coordinate types (scatter/bubble)
  - Applying colors from `ColorGroupModel`
  - Attaching axis IDs and dataset options

### `models_options.py` — Options System
- **`OptionsBase`** (abstract): A single key-value option with type coercion (text, number, boolean, json, array, function). Converts values to JSON via `get_json_value()`.
- **`OptionsParentBase`** (abstract): Mixin that reads related `options` and builds a nested dictionary from dot-separated labels (e.g., `hover.mode` → `{'hover': {'mode': ...}}`).
- **`OptionsGroupBase`** (abstract): Named, reusable group of options. Invalidates cache on save/delete.
- **`GlobalOptionsGroupModel`**: Site-scoped global Chart.js defaults. Provides `get_global_options()` and `get_global_colors()` class methods.
- **`ChartOptionsGroupModel`** / **`DatasetOptionsGroupModel`**: Reusable option groups for charts and datasets.
- **`ChartSpecificOptionsModel`** / **`DatasetSpecificOptionsModel`**: Per-instance inline options (FK to `ChartModel`/`DatasetModel`).

### `models_axes.py` — Axis Configuration
- **`AxisOptionsGroupModel`**: Defines a named axis with type (linear/logarithmic/category/time/radial), display mode, weight, and custom options. Generates axis dictionaries with slugified IDs.

### `models_colors.py` — Color Palettes
- **`ColorModel`**: Maps chart types + namespace labels to a list of colors.
- **`ColorGroupModel`**: Groups multiple `ColorModel` entries. Builds a nested dict: `{chart_type: {namespace: [colors]}}`.

### `consts.py` — Constants & Chart.js Option Definitions
- Chart type enum (`CHART_TYPES`), axis types, dataset formats, legend positions
- Functions to load Chart.js option schemas for admin select2 widgets

### `cms_plugins.py` — CMS Plugin Registration
- **`ChartJsPlugin`**: Registered CMS plugin for charts. Renders `chartjs.html` with JSON chart data and global options.
- **`DatasetPlugin`**: Child-only plugin (no render) for additional datasets.

### `forms.py` — Admin Forms
- **`DatasetInputForm`**: Handles table data input widget + CSV upload. Strips empty rows/columns.
- **`OptionsInlineFormBase`**: Validates option values against their declared type.
- **`ColorInputForm`**: Multi-select for chart types, labels, and color picker widget.

### `cache.py` — Caching Layer
- Optional dedicated cache backend (`DJANGOCMS_CHARTS_CACHE` setting)
- `get()`, `set()`, `delete()`, `clear_all()` functions keyed by `{class_name}_{id}`

### `utils.py` — Utility Functions
- `transpose()`: Transposes a 2D array
- `get_unique_list()`: Deduplicates dicts by key
- `color_variant()`: Lightens/darkens hex colors

### `admin.py` — Inline Admins
- Inline admin classes for chart/dataset/global/axis options and color entries

### `urls.py` / `views.py`
- AJAX endpoint for fetching Chart.js option labels dynamically

