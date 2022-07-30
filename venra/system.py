"""Vespa system apis

"""


from . import client
from . import config


def version_app():
    """Return the version string from the app server

    example:
    $ curl -s http://127.0.0.1:8080/state/v1/version | jq .
    {
        "version": "8.13.21"
    }
    """
    vc = client.get_vespa_client()
    vr = vc.get(f"{config.vespa_host_app}/state/v1/version").json()
    return vr["version"]


def version_cfg():
    """Return the version string from the app server

    example:
    $ curl -s http://127.0.0.1:19071/state/v1/version | jq .
    {
        "version": "8.13.21"
    }
    """
    vc = client.get_vespa_client()
    vr = vc.get(f"{config.vespa_host_cfg}/state/v1/version").json()
    return vr["version"]


