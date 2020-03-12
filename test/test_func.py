import requests

json_headers = {
    "Accept": "application/json"
}

json_post_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
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
        }]
    } ]
}

vega_spec_input = {
  "typeid": "line_chart",
  "x_axis_title": "Time",
  "y_axis_title": "Drug Dosage"
}

vega_spec_output = {
    "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
    "title": "Line chart",
    "description": "Time-series line chart",
    "width": "container",
    "height": "container",
    "autosize": { "resize": True },
    "data": { "name": "data" },
    "mark": "line",
    "encoding": {
        "x": {
            "field": "x",
            "type": "quantitative",
            "axis": { "title": "Time" }
        },
        "y": {
            "field": "y",
            "type": "quantitative",
            "axis": { "title": "Drug Dosage" }
        }
    }
}


def test_vega_spec():
    resp = requests.post("http://tx-vis:8080/vega_spec", headers=json_post_headers, json=vega_spec_input)

    assert resp.status_code == 200
    output = resp.json()
    assert output == vega_spec_output


def test_config():
    resp = requests.get("http://tx-vis:8080/config", headers=json_headers)

    assert resp.status_code == 200
    assert resp.json() == config


def test_ui():
    resp = requests.get("http://tx-vis:8080/ui")

    assert resp.status_code == 200
