"""venra.exceptions

A collection of exceptions which encapsulate various Vespa and http request
errors, to assist with application control flow.

"""


class VenraException(Exception):
    """A base exception for unexpected errors"""


class VespaCommunicationError(VenraException):
    """An error connecting to Vespa"""


class VespaRequestError(VenraException):
    """A general error as a result of making a request to Vespa"""


class VespaItemDoesNotExist(VenraException):
    """An error for attempted operation on an item which does not exist"""

