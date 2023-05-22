"""This module contains the core wrap errors."""
# pylint: disable=too-many-arguments

from __future__ import annotations

import json
from textwrap import dedent
from typing import Any, Dict, Optional

from polywrap_msgpack import msgpack_decode

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
        uri: Uri,
        method: str,
        message: str,
        invoke_args: Optional[Dict[str, Any]] = None,
        invoke_env: Optional[Dict[str, Any]] = None,
    ):
        """Initialize a new instance of WasmAbortError."""
        self.uri = uri
        self.method = method
        self.message = message

        self.invoke_args = (
            json.dumps(
                msgpack_decode(invoke_args)
                if isinstance(invoke_args, bytes)
                else invoke_args,
                indent=2,
            )
            if invoke_args is not None
            else None
        )
        self.invoke_env = (
            json.dumps(
                msgpack_decode(invoke_env)
                if isinstance(invoke_env, bytes)
                else invoke_env,
                indent=2,
            )
            if invoke_env is not None
            else None
        )

        super().__init__(
            dedent(
                f"""
                WrapAbortError: The following wrapper aborted execution with the given message:
                URI: {uri}
                Method: {method}
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


__all__ = ["WrapError", "WrapAbortError", "WrapInvocationError"]
