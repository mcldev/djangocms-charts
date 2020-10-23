# DjangoCMS_Charts


[![PyPI version](https://badge.fury.io/py/djangocms-charts.svg)](https://badge.fury.io/py/djangocms-charts)
[![PyPi downloads](https://pypip.in/d/djangocms-charts/badge.png)](https://crate.io/packages/djangocms-charts/)

A plugin for DjangoCMS that creates easy to use and fully customisable ChartJs (ver 2.x) charts - with a table and csv upload interface.

## Updates

- 3.0.0
    - **CAUTION** - This is a complete refactoring of DjangoCMS Charts to ChartJS version 2.x
    - ***All Models, Fields, and Options have changed***
    - ***Due to changes in ChartJS 1.x > 2.x - Not all Custom settings will be migrated***
    - The migrations attempt to bring over any settings changed from the default values from each previous chart.
    - ChartJS is enabled by default - update settings to disable as below
    - All chart types are now available in the ChartsJS Plugin
    - Multiple Datasets can be added as Child Plugins of the parent ChartJS Plugin
    - Global Options are added in the Admin, as required.
    - All Options come from the ChartJS object/dictionary and are using a Select2 list

## Quick start
1. Add 'djangocms_charts' to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djangocms_charts',
    ]

2. Run `python manage.py migrate` to create the djangocms_charts models.

3. Ensure you have your own version of jQuery added to block 'js'. See here: https://django-sekizai.readthedocs.io/en/latest/#example

4. Add a DjangoCMS ChartJS Plugin to your web page!

## Caching [Optional]
The queries and building up of each chart can be expensive for many options/data rows/charts etc. 
To speed this up set up a dedicated DjangoCMS Charts cache.
This **should be a unique cache** as it will require to be cleared after saving any charts object due to the complex relationship between all objects.

1. In `settings.py` add `DJANGOCMS_CHARTS_CACHE = 'djangocms_charts'` which should map to a unique cache.

2. In your `CACHES` add the charts cache - sample backend below - use your own cache system:
```
CACHES = {
    'default': {
        ...
    },
    'djangocms_charts':{
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'djangocms_charts',
        'TIMEOUT': CACHE_MIDDLEWARE_SECONDS,
        'OPTIONS': {
            'MAX_ENTRIES': 5000
        }
    },
}
```

## URLS [Optional]
If access to the JSON Vesion of the chart is required add the following to your `urls.py` :

```
urlpatterns = [
    ...
    url(r'^chartjs/', include('djangocms_charts.urls')),
    ...
]
```
The JSON view can then be accessed via:
 - Chart View: `[url]/chartjs/get_chart_as_json/[chart_id]/`
 - Global Options View: `[url]/get_global_options_as_json/[options_id]/`


## ChartJs-Sass [Optional]
All chart dataset colours (backgroundColor, borderColor, etc) can be set using CSS via ChartJS-Sass. This JS library will update any unspecified colors with those specified in the CSS and built using SASS.
For more details see: https://github.com/mcldev/ChartJS-Sass

1. To disable/enable, in `settings.py` add `DJANGOCMS_CHARTS_ENABLE_CHARTJS_SASS = True or False (default=True)` 


## Usage

### Chart Types
The following chart types can be selected with options (see below)
- Line
- Line XY (Scatter with line)
- Bar
- Horizontal Bar
- Radar
- Polar
- Pie
- Doughnut
- Bubble
- Scatter
- Mixed (see Multiple Datasets)


### Input Data
All input data will be used as below.
 
NB: Multiple datasets can be added as either:
- Dataset Plugins as child to each Chart Plugin (customisable colours/formats etc)
- Multiple rows or columns within a Chart input table (scriptable colours/formats)

```
    # Line, Bar, Radar, Doughnut, Pie, PolarArea
    # ------------------------------------------
    # Datasets in 'cols' > TRANSPOSED
    #       Label_1,    Label_2, ...
    # Jan-20    10      30
    # Feb-20    20      40
    # ...
    #
    # OR
    #
    # Datasets in 'rows'    > USES THIS FORMAT INTERNALLY
    #       Jan-20      Feb-20, ...
    # Label_1   10      20
    # Label_2   30      40
    # ...
    #
    # Bubble [r], Scatter, Line_XY
    # ----------------------------
    # [r - radius - is ignored for line and scatter]
    #
    # Datasets in 'cols' > TRANSPOSED
    #   x   10   20     ...
    #   y   30   40     ...
    #  [r]   5   10     ...
    #
    # OR
    #
    # Datasets in 'rows'    > USES THIS FORMAT INTERNALLY
    #   x,      y,      [r]
    #   10      30      5
    #   20      40      10
    #   ...
```

### Axes
https://www.chartjs.org/docs/latest/axes/

Multiple Axes can be added using X Axis or Y Axis. Each Axis can be used multiple times (e.g. Linear axis).
Options for Axes are set below.

### Multiple Datasets
https://www.chartjs.org/docs/latest/charts/mixed.html#drawing-order

Multiple datasets can be added as rows/columns of the main chart, or added as Dataset child plugins.
The rendering order for ChartJS is that the first dataset is top-most - this plugin prepends the subsequent child datasets so the last dataset is top-most.

### Mixed Types
https://www.chartjs.org/docs/latest/charts/mixed.html

Each child Dataset can have a different type, thus creating a Mixed Chart. 
**NB:** Some types do not mix well (Radar/Bar etc) - we make no validation on each possible combination.

## Dataset Colors
Dataset Color Groups can be specified as a user-friendly list of colors, with a click-and-drag sortable feature.

### Specifying the color group
Specifications for each group require the following:
- Type (select multiple types with Ctrl)
    - the Chart/Dataset type that these colors will be applied to
- Namespace Labels (select multiple types with Ctrl)
    - the dataset namespace labels that will use these colors
    - e.g. `backgroundColor, borderColor, pointBackgroundColor, ...`
- Colors 
    - a text list of **hex only** colors
    - these can be selected/edited/rearranged through the interface

### Application of Color Groups 
These color groups can then be applied as follows:
- Globally 
    - by assigning the color group to the Global Settings
    - any Chart/Dataset (without colors specified) will use these colors
- By Chart
    - all of the Chart datasets and any sub-datasets (without colors specified) will have these colors applied
- By Dataset
    - any Dataset can specifically use this Color Group 

### Color By Dataset or Series
The flag to set 'Color by Dataset' will do the following:
- Color by Dataset: `True`
    - Each individual Dataset will use one color from the color array based on its index
    - e.g. with a color array of `[red, green, blue]`
    ```
    #       Jan-20      Feb-20, ...
    # Label_1   10      20      <- red
    # Label_2   30      40      <- green
    # Label_3   50      60      <- blue
    ```
- Color by Series: `False`
    - Each individual Dataset will get the full color array to use for each element in Series
    - e.g. with a color array of `[red, green, blue]`
    ```
    #           Jan-20      Feb-20, ...
    # Label_1   10  <- red    20      <- green
    # Label_2   30  <- red    40      <- green
    # Label_3   50  <- red    60      <- green
    ```

## Options
https://www.chartjs.org/docs/latest/configuration/

Options are set in JavaScript using the settings provided by ChartJS - Use this documentation: https://www.chartjs.org/docs/latest/ 

The Options are assigned in ascending order of priority as:
- `Chart.defaults.global.<option>` - see GlobalOptionsGroup in Admin
- `chart.options.<option>` - see ChartOptions Group selectable for each chart
- `chart.options.<option>` - see ChartSpecificOptions assigned to each chart individually
- `dataset.<option>` - see DatasetOptionsGroup selectable for each dataset
- `dataset.<option>` - see DatasetSpecificOptions assigned to each dataset individually
- `chart.options.scales.<axes>.<option>` - see AxisOptionsGroup selectable for each axis 

### Option Input Types
https://www.chartjs.org/docs/latest/general/options.html

ChartJS accepts various input option formats, some can be scripted, functions, numbers, or text.
DjangoCMS Charts options can be input as any one of the following types:

**NB. there is no validation of input types - Errors will appear in the console** 
- text
    - Any form of text input, such as a colour. e.g.  `#28aece`
    - Sample output: `{"option_name": "#28aece"}`
- number
    - Either an integer or float can be input e.g. `2 or 3.5`
    - A float (with a '.') will be converted to float
    - Sample output: `{"option_name": 2}`  
- boolean
    - Text or number be cast to a boolean, can be any of `'true', 'false', 1, 0`
    - Sample output: `{"option_name": true}`
- json
    - Text to be parsed and loaded as valid Json, e.g. `['red', 'blue', 'green']`
    - Sample output: `{"option_name": ["red", "blue", "green"]}`
- array
    - Will split a string array into elements using the following (in order): 
        - `"\n"`  (new line)
        - `","`   (comma)
        - `"\t"`  (tab)
        - `" "`   (space)
    - Sample input: `red blue green`
    - Sample output: `{"option_name": ["red", "green", "blue"}]`
- function
    - A js function string that will be cleaned (new lines etc.) and injected into the code.
    - Can be a valid function name or complete function **without comments**
    - Sample: 
    ```
  function(context) {
    var index = context.dataIndex;
    var value = context.dataset.data[index];
    return value < 0 ? 'red' :
        index % 2 ? 'blue' :  
        'green';
    }
    ```

# More details on ChartJs
http://www.chartjs.org/
 
ChartJs is a dynamic JS charting application giving users an interactive and visually appealing chart in an html 5 canvas. Each type of chart is available:

