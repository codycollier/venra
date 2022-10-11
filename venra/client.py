"""venra.client

A module for creating and managing the internal venra http client. 

This is a thin wrapper around a requests session client, allowing
for cross cutting access throughout the venra package.

"""

import functools

import requests

from . import config
from . import exceptions


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


def _enclose_request(fn):
    """An envelope to handle all http requests in a Venra speciic manner

    The stack of requests + urrllib3 can be a bit noisy with errors and stack
    traces. Venra aims to allow for simple control flow, so this helper
    wraps the call to requests and returns simpler exceptions and messages.
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwds):

        try:
            return fn(*args, **kwds)

        except requests.exceptions.Timeout:
            err = f"Timeout communicating with Vespa"
            err += f"\n  timeout: {config.timeout_s} seconds"
            err += f"\n      url: {args[1]}"
            raise exceptions.VespaCommunicationError(err)

        except requests.exceptions.RequestException as original_err:
            err = f"Unable to communicate with vespa"
            err += f"\n  upstream err: {original_err}"
            raise exceptions.VespaCommunicationError(err)

    return wrapper


def _init_client():
    """Initialize and return a new requests based client"""

    vc = requests.Session()

    # set a default timeout for all requests
    vc.request = functools.partial(vc.request, timeout=config.timeout_s)

    # wrapp all requests in a Venra specific try/except handler
    vc.request = _enclose_request(vc.request)

    return vc

