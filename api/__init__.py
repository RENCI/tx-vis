import subprocess
import json

type_mapping_dict = {
    'line_chart': 'api/templates/vega-lite-line-chart.dhall',
    'multiple_line_chart': 'api/templates/vega-lite-multi-line-chart.dhall',
    'area_chart': 'api/templates/vega-lite-area-chart.dhall',
    'scatter_plot': 'api/templates/vega-lite-scatter-plot.dhall',
    'multiple_scatter_plot': 'api/templates/vega-lite-multi-scatter-plot.dhall',
    'histogram': 'api/templates/vega-lite-histogram.dhall',
    'dosing_plot': 'api/templates/vega-lite-dosing.dhall'
}

config = {
    "title": "Visualization spec generator",
    "piid": "tx-vis",
    "pluginType": "c",
    "pluginParameters": [ {
        "typeid": "line_chart",
        "typeDescription": "Line chart visualization type",
        "legalParameters": [ {
            "type": "string",
            "name": "x_axis_title"
        },
        {
            "type": "string",
            "name": "y_axis_title"
        },
        {
          "type": "string",
          "name": "chart_title"
        },
        {
          "type": "string",
          "name": "chart_description"
        } ]
    },
    {
        "typeid": "Multiple_line_chart",
        "typeDescription": "Multiple Line chart visualization type",
        "legalParameters": [{
            "type": "string",
            "name": "x_axis_title"
        },
        {
            "type": "string",
            "name": "y_axis_title"
        },
        {
          "type": "string",
          "name": "chart_title"
        },
        {
          "type": "string",
          "name": "chart_description"
        } ]
    },
    {
        "typeid": "area_chart",
        "typeDescription": "Area chart visualization type",
        "legalParameters": [{
            "type": "string",
            "name": "x_axis_title"
        },
        {
            "type": "string",
            "name": "y_axis_title"
        },
        {
          "type": "string",
          "name": "chart_title"
        },
        {
          "type": "string",
          "name": "chart_description"
        }]
    },
    {
        "typeid": "scatter_plot",
        "typeDescription": "scatter plot visualization type",
        "legalParameters": [{
            "type": "string",
            "name": "x_axis_title"
        },
        {
            "type": "string",
            "name": "y_axis_title"
        },
        {
          "type": "string",
          "name": "chart_title"
        },
        {
          "type": "string",
          "name": "chart_description"
        }]
    },
    {
        "typeid": "multiple_scatter_plot",
        "typeDescription": "multiple scatter plot visualization type",
        "legalParameters": [{
            "type": "string",
            "name": "x_axis_title"
        },
        {
            "type": "string",
            "name": "y_axis_title"
        },
        {
          "type": "string",
          "name": "chart_title"
        },
        {
          "type": "string",
          "name": "chart_description"
        }]
    },
    {
        "typeid": "histogram",
        "typeDescription": "histogram visualization type",
        "legalParameters": [{
            "type": "string",
            "name": "x_axis_title"
        },
        {
            "type": "string",
            "name": "y_axis_title"
        },
        {
          "type": "string",
          "name": "chart_title"
        },
        {
          "type": "string",
          "name": "chart_description"
        }]
    },
    {
        "typeid": "dosing_plot",
        "typeDescription": "dosing plot visualization type",
        "legalParameters": [{
            "type": "string",
            "name": "x_axis_title"
        },
        {
            "type": "string",
            "name": "y_axis_title"
        },
        {
          "type": "string",
          "name": "chart_title"
        },
        {
          "type": "string",
          "name": "chart_description"
        }]
    } ]
}


def get_vega_spec_util(type="line_chart", x_axis_title="x axis", y_axis_title="y axis",
                       title="Line chart", desc="Time-series line chart"):

    if type in type_mapping_dict:
        template_fn = type_mapping_dict[type]
    else:
        template_fn = type_mapping_dict['line_chart']

    with open(template_fn, 'r') as fp:
        template_data = fp.read().replace('\n', '')
        let_string = 'let x_axis_title="' + x_axis_title + '" let y_axis_title="' + \
                     y_axis_title + '" let chart_title="' + title + \
                     '" let chart_desc="' + desc + '" in '
        data = '{} {}'.format(let_string, template_data)
        cmd = "echo '" + data + "' | dhall-to-json"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if stderr:
            raise RuntimeError(stderr)

        return stdout

    raise FileNotFoundError("Cannot read dhall configuration template file")


def get_config():
    return config


def get_vega_spec(body):
    type_id = body['typeid'] if 'typeid' in body else 'line_chart'
    x_axis_title = body['x_axis_title'] if 'x_axis_title' in body else 'x axis'
    y_axis_title = body['y_axis_title'] if 'y_axis_title' in body else 'y axis'
    title = body['chart_title'] if 'chart_title' in body else 'Line chart'
    desc = body['chart_description'] if 'chart_description' in body else 'Time-series line chart'
    vis_spec = get_vega_spec_util(type=type_id, x_axis_title=x_axis_title,
                                  y_axis_title=y_axis_title, title=title, desc=desc)
    # convert returned bytes to str
    vis_spec = vis_spec.decode("utf-8")

    return json.loads(vis_spec)
