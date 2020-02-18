import requests

json_headers = {
    "Accept": "application/json"
}

config = {
    "title": "DOAC variable mapper",
    "pluginType": "m",
    "pluginTypeTitle": "Mapping",
    "pluginSelectors": []
}


def test_config():
    resp = requests.get("http://pdspi-example:8080/config", headers=json_headers)

    assert resp.status_code == 200
    assert resp.json() == config

    
def test_ui():
    resp = requests.get("http://pdspi-example:8080/ui")

    assert resp.status_code == 200
