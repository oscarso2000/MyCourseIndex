"""Exceptions module specialized for the Piazza client api."""


class PiazzaRequestError(Exception):
    """PiazzaRequestError is a request error to piazza logic api"""


class AuthenticationError(Exception):
    """Authentication Error represents error attempting to use credentials"""


class NotAuthenticatedError(Exception):
    """NotAuthenticatedError is an attempted access w/o correct permissions"""


class NoClassIDError(Exception):
    """NoClassIDError is no class id being provided to the api"""
    