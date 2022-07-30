"""Vespa client

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



