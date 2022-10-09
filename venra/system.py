"""venra.system

A module which aggregates access to the wide variety of Vespa apis which 
generally provide system type information.

Venra is generally focused on client interaction with running Vespa systems,
so this module is currently focused on read-only access to system information.


Related Vespa documentation:
* https://docs.vespa.ai/en/reference/state-v1.html
* https://docs.vespa.ai/en/reference/deploy-rest-api-v2.html
* https://docs.vespa.ai/en/reference/config-rest-api-v2.html
* https://docs.vespa.ai/en/reference/application-v2-tenant.html
* https://docs.vespa.ai/en/reference/cluster-v2.html
* https://docs.vespa.ai/en/reference/metrics-v2.html


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


