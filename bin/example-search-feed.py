#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Sample program to iterate through docs via visit
#
#

import sys

import venra


if __name__ == "__main__":

    # usage
    if len(sys.argv) != 3:
        print("")
        print("Usage:")
        print("> ./example-search-feed.py <doctype> <query>")
        print("")
        print("Example:")
        print('> export VESPA_HOST_APP="http://192.168.100.30:8080"')
        print("> ./example-search-feed.py fruitdocs orange")
        print("")
        sys.exit(1)

    # params
    doctype = sys.argv[1]
    query = sys.argv[2]

    # load host env vars
    venra.config.load_overrides_from_env()

    # define query
    qdata = {}
    qdata["yql"] = f"select * from sources {doctype} where userQuery();"
    qdata["hits"] = 250
    qdata["model.queryString"] = f"{query}"
    qdata["model.type"] = "weakAnd"


    # visit and print to the limit
    limit = 5000
    for i, d in enumerate(venra.search.feed(qdata)):
        print(f"::> {d['id']} ({len(d['fields'])})")
        if i > limit:
            print(f"reached limit: {limit}")
            break


