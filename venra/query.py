"""Vespa search api

"""

import requests

from . import client
from . import config



def feed(qdata):
    """Yield all docs for a given query

    example qdata:
    qdata = {}
    qdata["yql"] = f"select * from sources mydocs where userQuery();"
    qdata["hits"] = 3
    qdata["timeout"] = "3300ms"
    ...

    """
    search_base_uri = f"{config.vespa_host_app}/search/"

    # ensure offset is explicitly set
    if "offset" not in qdata:
        qdata["offset"] = 0

    # initial call
    vc = client.get_vespa_client()
    vr = requests.post(f"{search_base_uri}", json=qdata).json()
    total_results = vr["root"]["fields"]["totalCount"]

    # page through results
    doc_count = 0
    while True:

        # extract the docs from the response structure
        try:
            docs = vr["root"]["children"]
        except KeyError:
            print("Error retrieving results")
            print(vr)
            break

        # yield each doc from the search results
        for d in docs:
            doc_count += 1
            yield d

        # stop if we reached the end of the results
        if doc_count >= total_results:
            break

        # get next page of results
        qdata["offset"] += 1
        vr = requests.post(f"{search_base_uri}", json=qdata).json()

    return


