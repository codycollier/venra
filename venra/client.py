"""venra.client

A module for creating and managing the venra client. 

This is generally a thin wrapper around a requests session client, allowing
for cross cutting access across the venra package.


"""

import requests

from . import config


vclient = None


def reset():
    """Remove initialized client"""
    global vclient
    vclient = None


def get_vespa_client():
    """Get or create a vespa client and return"""

    global vclient

    # initialize session if not already done
    if vclient is None:
        vclient = requests.Session()

    return vclient



