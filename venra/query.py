"""venra.query

A module for interacting with the Vespa query api


Related Vespa documentation:
* https://docs.vespa.ai/en/query-api.html
* https://docs.vespa.ai/en/reference/query-api-reference.html


"""

from collections import OrderedDict
import time

import requests

from . import client
from . import config
from . import exceptions


def _api_err_check(response):
    """Error handling for http responses unique to the query api

    Related Vespa documentation:
    * https://docs.vespa.ai/en/reference/query-api-reference.html#http-status-codes
    """
    if response.status_code != 200:
        err = f"unexpected response\n"
        err += f"  response code: {response.status_code}\n"
        err += f"  response  url: {response.url}\n"
        err += f"  response body: {response.text}\n"
        raise exceptions.VespaRequestError(err)


def _vespa_post(qdata):
    """Internal wrapper for search api http call handling"""
    base_uri = f"{config.vespa_host_app}/search/"
    vc = client.get_vespa_client()
    vr = vc.post(f"{base_uri}", json=qdata)
    _api_err_check(vr)
    vr = vr.json()
    return vr


def search(qdata):
    """Run a search with the given parameters and return the complete results

    The return val is the complete query response json loaded as a dictionary
    """
    qstarted = time.time()
    qresults = _vespa_post(qdata)
    qstopped = time.time()
    elapsed = qstopped - qstarted
    qresults["venra"] = {"elapsed_ms": elapsed}
    return qresults


def extract_metrics(qresults):
    """Return key metrics, timings, etc from the search response

    This is an optional convenience function for extracting various key metrics
    from the query response.
    """
    qmet = {}
    qmet["matchcount"] = qresults["root"]["fields"]["totalCount"]
    qmet["totalcount"] = qresults["root"]["coverage"]["documents"]
    qmet["coverage"] = qresults["root"]["coverage"]["coverage"]
    if "timing" in qresults:
        qmet["querytime"] = qresults["timing"]["querytime"]
        qmet["searchtime"] = qresults["timing"]["searchtime"]
        qmet["summaryfetchtime"] = qresults["timing"]["summaryfetchtime"]
    qmet["elapsed_ms"] = round(1000 * qresults["venra"]["elapsed_ms"], 3)
    return qmet


def extract_docs(qresults, fields_only=True):
    """Return an ordered list of doc fields from a search response

    This is an optional convenience function for the common action of extracting
    an ordered list of the docs from the query response.
    """
    docs = []

    # return early if results are empty
    if not qresults or qresults["root"]["fields"]["totalCount"] == 0:
        return docs

    # collect the docs
    for result in qresults["root"]["children"]:

        # skip group node
        if result["id"] == "group:root:0":
            continue

        # add to results
        if fields_only:
            docs.append(result["fields"])
        else:
            docs.append(result)

    return docs


def extract_groups(qresults):
    """Extract the groups from a query response

    This is an optional convenience function. It will build a dictionary which
    then contains each grouplist, which themselves are ordered dicts. This is
    useful for extracting grouping for easy access to build facets etc.

    example:
     select ... | all(group(time.date(some_date)) order(-max(some_date)) max(10) each(output(count())) as(myfacet) )

    return groups:
     groups["myfacet"] = OrderedDict()
     groups["myfacet"]["2022-3-14"] = 108
     groups["myfacet"]["2022-3-13"] = 300
     groups["myfacet"]["2022-3-12"] = 278
     ...
    """
    groups = {}

    # find the root node for the groups
    group_node = None
    for result in qresults["root"]["children"]:
        if result["id"] == "group:root:0":
            group_node = result
            break

    # return early if there is no group info
    if group_node is None:
        return groups

    # collect the results for each grouplist
    for grouplist in group_node["children"]:
        gl = OrderedDict()
        for group in grouplist["children"]:
            gl[group["value"]] = group["fields"]  # ex: item["fields"]["count()"]
        groups[grouplist["label"]] = gl

    return groups


def extract_group_pairs(groups, label, field_name="count()"):
    """From an extracted grouplist, return a list of (value, count) tuples

    This is an optional convenience function for extracting the fundamental
    (key, value) pairs for a grouping/facet.

    Given:
     groups["bazgroup"] = OrderedDict()
     groups["bazgroup"]["bar"]["fields"]["count()"] = 3
     groups["bazgroup"]["foo"]["fields"]["count()"] = 1
     groups["myfacet"] = OrderedDict()
     groups["myfacet"]["2022-3-14"]["fields"]["count()"] = 108
     groups["myfacet"]["2022-3-13"]["fields"]["count()"] = 300
     groups["myfacet"]["2022-3-12"]["fields"]["count()"] = 278

    Calling extract_group_pairs(groups, "myfacet", "count()")
    Returns:
     [("2022-3-14", 108), ("2022-3-13", 300), ("2022-3-12", 278)]
    """
    pairs = []
    for k,f in groups[label].items():
        pairs.append((k, f[field_name]))
    return pairs


def feed(qdata, fields_only=True):
    """Yield all docs for a given query

    example qdata:
    qdata = {}
    qdata["yql"] = f"select * from sources mydocs where userQuery();"
    qdata["hits"] = 3
    qdata["timeout"] = "3300ms"
    ...

    """
    # ensure offset is explicitly set
    if "offset" not in qdata:
        qdata["offset"] = 0

    # initial query
    qresults = search(qdata)
    total_results = qresults["root"]["fields"]["totalCount"]

    # page through results
    doc_count = 0
    while True:

        # extract the docs from the response structure
        docs = extract_docs(qresults, fields_only)

        # yield each doc from the search results
        for d in docs:
            doc_count += 1
            yield d

        # stop if we reached the end of the results
        if doc_count >= total_results:
            break

        # get next page of results
        qdata["offset"] += 1
        qresults = search(qdata)

    return


