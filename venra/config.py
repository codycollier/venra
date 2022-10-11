"""venra.config

A module for accessing and managing config for venra itself.

The default configuration targets a local, single-node instance of Vespa with
all standard ports and configuration.


"""

import os


#------------------------------------------------------------------------------
# Configuration
#------------------------------------------------------------------------------

# Main endpoints
vespa_host_cfg = "http://127.0.0.1:19071"
vespa_host_app = "http://127.0.0.1:8080"

# http client
timeout_s = 3.5


#------------------------------------------------------------------------------
# Config management
#------------------------------------------------------------------------------

def load_overrides_from_env():
    """Load any override configuration values from env vars

    example:
    > export VESPA_HOST="192.168.1.50"
    """

    if "VESPA_HOST_CFG" in os.environ:
        global vespa_host_cfg
        vespa_host_cfg = os.environ["VESPA_HOST_CFG"]

    if "VESPA_HOST_APP" in os.environ:
        global vespa_host_app
        vespa_host_app = os.environ["VESPA_HOST_APP"]

    return


def load_overrides_from_file():
    """Load any override configuration values from config file

    """
    pass

