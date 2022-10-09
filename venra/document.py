"""venra.document

A module for interacting with the Vespa /document/v1 api.


Related Vespa documentation:
* https://docs.vespa.ai/en/document-v1-api-guide.html
* https://docs.vespa.ai/en/reference/document-v1-api-reference.html
* https://docs.vespa.ai/en/reference/document-json-format.html
* https://docs.vespa.ai/en/reference/document-json-format.html#document-operations


"""

import json

from . import client
from . import config


def get(namespace, doctype, docid):
    """Retrieve and return a document

    """
    base_uri = f"{config.vespa_host_app}/document/v1/{namespace}/{doctype}/docid/{docid}"
    vc = client.get_vespa_client()
    doc = vc.get(f"{base_uri}")
    return doc


def put(namespace, doctype, docid, doc):
    """Add or update a whole document

    """
    base_uri = f"{config.vespa_host_app}/document/v1/{namespace}/{doctype}/docid/{docid}"
    vc = client.get_vespa_client()
    doc_fields = {"fields": doc}
    vr = vc.post(f"{base_uri}", data=json.dumps(doc_fields))
    return vr


def update(namespace, doctype, docid, operations):
    """Apply a partial update using the assign, add, or remove operator

    operations = [("assign", "field_name_here", "field_value_here"), ...]

    reference:
    * https://docs.vespa.ai/en/reference/document-json-format.html

    Example:
    * https://docs.vespa.ai/en/reference/document-json-format.html#assign-map-field
    {
        "update": "id:mynamespace:food::example",
        "fields": {
            "my_food_scores{Strawberries}": { "assign": "Delicious!" }
        }
    }
    """
    base_uri = f"{config.vespa_host_app}/document/v1/{namespace}/{doctype}/docid/{docid}"
    partial_update = {"fields": {}}
    for operation, field_name, field_value in operations:
        partial_update["fields"][field_name] = {operation: field_value}

    vc = client.get_vespa_client()
    vr = vc.put(f"{base_uri}", data=json.dumps(partial_update))

    return vr


def remove(namespace, doctype, docid):
    """Delete a document

    """
    base_uri = f"{config.vespa_host_app}/document/v1/{namespace}/{doctype}/docid/{docid}"
    vc = client.get_vespa_client()
    vr = vc.delete(f"{base_uri}")
    return vr


