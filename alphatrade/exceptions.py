# -*- coding: utf-8 -*-
"""
    exceptions.py

    Exceptions raised by the Alpha Trade client.

    :license: see LICENSE for details.
"""


class AlphaException(Exception):
    """
    Base exception class representing a Alpha Trade client exception.

    Every specific Alpha Trade client exception is a subclass of this
    and  exposes two instance variables `.code` (HTTP error code)
    and `.message` (error text).
    """

    def __init__(self, message, code=500):
        """Initialize the exception."""
        super(AlphaException, self).__init__(message)
        self.code = code


class GeneralException(AlphaException):
    """An unclassified, general error. Default code is 500."""

    def __init__(self, message, code=500):
        """Initialize the exception."""
        super(GeneralException, self).__init__(message, code)


class TokenException(AlphaException):
    """Represents all token and authentication related errors. Default code is 403."""

    def __init__(self, message, code=403):
        """Initialize the exception."""
        super(TokenException, self).__init__(message, code)


class PermissionException(AlphaException):
    """Represents permission denied exceptions for certain calls. Default code is 403."""

    def __init__(self, message, code=403):
        """Initialize the exception."""
        super(PermissionException, self).__init__(message, code)


class OrderException(AlphaException):
    """Represents all order placement and manipulation errors. Default code is 500."""

    def __init__(self, message, code=500):
        """Initialize the exception."""
        super(OrderException, self).__init__(message, code)


class InputException(AlphaException):
    """Represents user input errors such as missing and invalid parameters. Default code is 400."""

    def __init__(self, message, code=400):
        """Initialize the exception."""
        super(InputException, self).__init__(message, code)


class DataException(AlphaException):
    """Represents a bad response from the backend Order Management System (OMS). Default code is 502."""

    def __init__(self, message, code=502):
        """Initialize the exception."""
        super(DataException, self).__init__(message, code)


class NetworkException(AlphaException):
    """Represents a network issue between Alpha Trade and the backend Order Management System (OMS). Default code is 503."""

    def __init__(self, message, code=503):
        """Initialize the exception."""
        super(NetworkException, self).__init__(message, code)
