"""venra.client

A module for creating and managing the internal venra http client. 

This is a thin wrapper around a requests session client, allowing
for cross cutting access throughout the venra package.

"""

import functools

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
    if vclient is None:
        vclient = _init_client()
    return vclient


def _init_client():
    """Initialize and return a new requests client"""
    vc = requests.Session()

    # set a default timeout for all requests
    vc.request = functools.partial(vc.request, timeout=config.timeout_s)

    return vc

