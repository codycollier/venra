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
        print("> ./example-visit-feed.py <namespace> <doctype>")
        print("")
        print("Example:")
        print('> export VESPA_HOST_APP="http://192.168.100.30:8080"')
        print("> ./example-visit-feed.py fruitdocs orange")
        print("")
        sys.exit(1)

    # params
    namespace = sys.argv[1]
    doctype = sys.argv[2]

    # load host env vars
    venra.config.load_overrides_from_env()

    # visit and print to the limit
    limit = 5000
    for i, d in enumerate(venra.visit.feed(namespace, doctype, fields_only=False)):
        if i > limit:
            print(f"reached limit: {limit}")
            break
        print(f"::> {d['id']} (fields:{len(d['fields'])})")


