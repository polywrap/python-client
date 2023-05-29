"""This module contains the core wrap errors."""
# pylint: disable=too-many-arguments

from __future__ import annotations

import json
from textwrap import dedent
from typing import Optional

from polywrap_msgpack import msgpack_decode

from .invoke_options import InvokeOptions
from .uri import Uri


class WrapError(Exception):
    """Base class for all exceptions related to wrappers."""


class WrapAbortError(WrapError):
    """Raises when a wrapper aborts execution.

    Attributes:
        invoke_options (InvokeOptions): InvokeOptions for the invocation\
            that was aborted.
        message: The message provided by the wrapper.
    """

    uri: Uri
    method: str
    message: str
    invoke_args: Optional[str] = None
    invoke_env: Optional[str] = None

    def __init__(
        self,
        invoke_options: InvokeOptions,
        message: str,
    ):
        """Initialize a new instance of WasmAbortError."""
        self.uri = invoke_options.uri
        self.method = invoke_options.method
        self.message = message

        self.invoke_args = (
            json.dumps(
                msgpack_decode(invoke_options.args)
                if isinstance(invoke_options.args, bytes)
                else invoke_options.args,
                indent=2,
            )
            if invoke_options.args is not None
            else None
        )
        self.invoke_env = (
            json.dumps(
                msgpack_decode(invoke_options.env)
                if isinstance(invoke_options.env, bytes)
                else invoke_options.env,
                indent=2,
            )
            if invoke_options.env is not None
            else None
        )

        super().__init__(
            dedent(
                f"""
                WrapAbortError: The following wrapper aborted execution with the given message:
                URI: {invoke_options.uri}
                Method: {invoke_options.method}
                Args: {self.invoke_args}
                env: {self.invoke_env}
                Message: {message}
                """
            )
        )


class WrapInvocationError(WrapAbortError):
    """Raises when there is an error invoking a wrapper.

    Attributes:
        invoke_options (InvokeOptions): InvokeOptions for the invocation \
            that was aborted.
        message: The message provided by the wrapper.
    """


class WrapGetImplementationsError(WrapError):
    """Raises when there is an error getting implementations of an interface.
    
    Attributes:
        uri (Uri): URI of the interface.
        message: The message provided by the wrapper.
    """

    uri: Uri
    message: str

    def __init__(self, uri: Uri, message: str):
        """Initialize a new instance of WrapGetImplementationsError."""
        self.uri = uri
        self.message = message

        super().__init__(
            dedent(
                f"""
                WrapGetImplementationsError: Failed to get implementations of \
                    the following interface URI with the given message:
                URI: {uri}
                Message: {message}
                """
            )
        )


__all__ = ["WrapError", "WrapAbortError", "WrapInvocationError", "WrapGetImplementationsError"]
