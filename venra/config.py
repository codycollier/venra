"""Configuration values, access, and management

The default configuration targets a local, single-node instance of Vespa with
all standard ports and configuration.
"""

import os


#------------------------------------------------------------------------------
# Configuration
#------------------------------------------------------------------------------

# Vespa
vespa_host = "127.0.0.1"
vespa_port_cfg = "19071"
vespa_port_app = "8080"

# Venra
baz = True


#------------------------------------------------------------------------------
# Config management
#------------------------------------------------------------------------------

def load_overrides_from_env():
    """Load any override configuration values from env vars

    example:
    > export VESPA_HOST="192.168.1.50"
    """

    if "VESPA_HOST" in os.environ:
        global vespa_host
        vespa_host = os.environ["VESPA_HOST"]

    if "VESPA_PORT_CFG" in os.environ:
        global vespa_port_cfg
        vespa_port_cfg = os.environ["VESPA_PORT_CFG"]

    if "VESPA_PORT_APP" in os.environ:
        global vespa_port_app
        vespa_port_app = os.environ["VESPA_PORT_APP"]

    return


def load_overrides_from_file():
    """Load any override configuration values from config file

    """
    pass

