"""venra.visit

Implementation for the visit subset of the document api


Vespa documentation:
* https://docs.vespa.ai/en/content/visiting.html
* https://docs.vespa.ai/en/reference/document-v1-api-reference.html#visit


"""


from . import client
from . import config
from . import exceptions


def _vespa_get(namespace, doctype, selection=None, continuation=None):
    """Internal wrapper for visit api http call handling"""
    base_uri = f"{config.vespa_host_app}/document/v1/{namespace}/{doctype}/docid"

    vc = client.get_vespa_client()

    if selection:
        vr = vc.get(f"{base_uri}?selection={selection}").json()
    elif continuation:
        vr = vc.get(f"{base_uri}?continuation={continuation}").json()
    else:
        vr = vc.get(f"{base_uri}").json()

    return vr


def feed(namespace, doctype, selection=None):
    """Yield all docs of a given type and selection

    """

    # initial call
    vr = _vespa_get(namespace, doctype, selection, None)

    # page through results
    while True:

        # yield each doc from the results
        for d in vr.get("documents", []):
            yield d

        # check for continuation / more results
        continuation = vr.get("continuation", False)
        if not continuation:
            break

        # retrieve the next set of results
        vr = _vespa_get(namespace, doctype, None, continuation)

    return

