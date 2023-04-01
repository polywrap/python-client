"""This module contains the core wrap errors."""

import json
from textwrap import dedent
from typing import Generic, TypeVar

from polywrap_msgpack import msgpack_decode

from .options.invoke_options import InvokeOptions
from .uri_like import UriLike

TUriLike = TypeVar("TUriLike", bound=UriLike)


class WrapError(Exception):
    """Base class for all exceptions related to wrappers."""


class WrapAbortError(Generic[TUriLike], WrapError):
    """Raises when a wrapper aborts execution.

    Attributes:
        invoke_options (InvokeOptions): InvokeOptions for the invocation\
            that was aborted.
        message: The message provided by the wrapper.
    """

    invoke_options: InvokeOptions[TUriLike]
    message: str

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        invoke_options: InvokeOptions[TUriLike],
        message: str,
    ):
        """Initialize a new instance of WasmAbortError."""
        self.invoke_options = invoke_options
        self.message = message

        invoke_args = (
            json.dumps(
                msgpack_decode(invoke_options.args)
                if isinstance(invoke_options.args, bytes)
                else invoke_options.args,
                indent=2,
            )
            if invoke_options.args is not None
            else None
        )
        invoke_env = (
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
                Args: {invoke_args}
                env: {invoke_env}
                Message: {message}
                """
            )
        )


class WrapInvocationError(WrapAbortError[TUriLike]):
    """Raises when there is an error invoking a wrapper.

    Attributes:
        invoke_options (InvokeOptions): InvokeOptions for the invocation \
            that was aborted.
        message: The message provided by the wrapper.
    """
