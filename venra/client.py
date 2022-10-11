"""venra.client

A module for creating and managing the internal venra http client. 

This is a thin wrapper around a requests session client, allowing
for cross cutting access throughout the venra package.

"""

import requests

from . import config


# TODO - switch to a thread-local cache
vclient = None


def reset():
    """Remove initialized client"""
    global vclient
    vclient = None


def get_vespa_client():
    """Get or create a vespa http client and return"""

    global vclient

    # initialize session if not already done
    if vclient is None:
        vclient = requests.Session()

    return vclient



