"""Vespa document api

"""

import json

from . import client
from . import config



def partial_update(namespace, doctype, docid, operations):
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


