"""venra.exceptions

A collection of exceptions which encapsulate various Vespa and http request
errors, to assist with application control flow.

"""


class VespaException(Exception):
    """A base exception for unexpected errors"""


class VespaConnectionError(VespaException):
    """An error connecting to Vespa"""


class VespaCallError(VespaException):
    """A general error making a call to Vespa"""


class VespaItemDoesNotExist(VespaException):
    """An error for attempted operation on an item which does not exist"""

