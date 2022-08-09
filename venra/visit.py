"""Vespa visit api

"""


from . import client
from . import config


def feed(namespace, doctype, selection=None):
    """Yield all docs of a given type and selection

    """
    visit_base_uri = f"{config.vespa_host_app}/document/v1/{namespace}/{doctype}/docid"

    # initial call
    vc = client.get_vespa_client()
    if selection:
        vr = vc.get(f"{visit_base_uri}?selection={selection}").json()
    else:
        vr = vc.get(f"{visit_base_uri}").json()

    # page through results
    while True:
        for d in vr.get("documents", []):
            yield d
        continuation = vr.get("continuation", False)
        if continuation:
            vr = vc.get(f"{visit_base_uri}?continuation={continuation}").json()
        else:
            break

    return

