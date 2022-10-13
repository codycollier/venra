"""venra.document

A module for interacting with the Vespa /document/v1 api.


Related Vespa documentation:
* https://docs.vespa.ai/en/document-v1-api-guide.html
* https://docs.vespa.ai/en/reference/document-v1-api-reference.html
* https://docs.vespa.ai/en/reference/document-json-format.html
* https://docs.vespa.ai/en/reference/document-json-format.html#document-operations
* https://docs.vespa.ai/en/documents.html#fieldsets


"""

import json

from . import client
from . import config
from . import exceptions


def _api_err_check(response):
    """Error handling for http responses unique to the document api

    Related Vespa documentation:
    * https://docs.vespa.ai/en/reference/document-v1-api-reference.html#http-status-codes
    """

    if response.status_code == 404:
        err = f"{response.url}"
        raise exceptions.VespaItemDoesNotExist(err)

    elif response.status_code != 200:
        err = f"unexpected response\n"
        err += f"  response code: {response.status_code}\n"
        err += f"  response  url: {response.url}\n"
        err += f"  response body: {response.text}\n"
        raise exceptions.VespaRequestError(err)


def _vespa_get(namespace, doctype, docid, fieldset="all"):
    """Internal wrapper for document api and http get handling"""
    base_uri = f"{config.vespa_host_app}/document/v1/{namespace}/{doctype}/docid/{docid}?fieldSet=[{fieldset}]"
    vc = client.get_vespa_client()
    vr = vc.get(f"{base_uri}")
    _api_err_check(vr)
    vr = vr.json()
    return vr


def _vespa_post(namespace, doctype, docid, doc):
    """Internal wrapper for document api and http post handling"""
    base_uri = f"{config.vespa_host_app}/document/v1/{namespace}/{doctype}/docid/{docid}"
    vc = client.get_vespa_client()
    vr = vc.post(f"{base_uri}", json=doc)
    _api_err_check(vr)
    return


def _vespa_put(namespace, doctype, docid, update):
    """Internal wrapper for document api and http put handling"""
    base_uri = f"{config.vespa_host_app}/document/v1/{namespace}/{doctype}/docid/{docid}"
    vc = client.get_vespa_client()
    vr = vc.put(f"{base_uri}", json=update)
    _api_err_check(vr)
    return


def _vespa_delete(namespace, doctype, docid):
    """Internal wrapper for document api and http delete handling"""
    base_uri = f"{config.vespa_host_app}/document/v1/{namespace}/{doctype}/docid/{docid}"
    vc = client.get_vespa_client()
    vr = vc.delete(f"{base_uri}")
    _api_err_check(vr)
    return


def get(namespace, doctype, docid, fieldset="all", fields_only=True):
    """Retrieve and return a document"""
    doc = _vespa_get(namespace, doctype, docid, fieldset)
    if fields_only:
        doc = doc["fields"]
    return doc


def put(namespace, doctype, docid, doc):
    """Add or update a whole document"""
    doc_fields = {"fields": doc}
    _vespa_post(namespace, doctype, docid, doc_fields)
    return True


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
    partial_update = {"fields": {}}
    for operation, field_name, field_value in operations:
        partial_update["fields"][field_name] = {operation: field_value}
    _vespa_put(namespace, doctype, docid, partial_update)
    return True


def remove(namespace, doctype, docid):
    """Delete a document"""
    _vespa_delete(namespace, doctype, docid)
    return True


