"""This module contains the RequestSynchronizerResolver."""
from asyncio import Future, ensure_future
from dataclasses import dataclass
from typing import Optional, Union

from polywrap_core import (
    Dict,
    InvokerClient,
    IUriResolutionContext,
    Uri,
    UriPackageOrWrapper,
    UriResolver,
)

from ...types import UriResolutionStep


@dataclass(kw_only=True, slots=True)
class RequestSynchronizerResolverOptions:
    """Defines the options for the RequestSynchronizerResolver.

    Attributes:
        should_ignore_cache (Optional[bool]): Whether to ignore the cache.\
            Defaults to False.
    """

    should_ignore_cache: Optional[bool]


class RequestSynchronizerResolver(UriResolver):
    """Defines a resolver that synchronizes requests.

    This resolver synchronizes requests to the same uri.\
        If a request is already in progress, it returns the future\
        of the existing request.\
        If a request is not in progress, it creates a new request\
        and returns the future of the new request.
    
    Attributes:
        existing_requests (Dict[Uri, Future[UriPackageOrWrapper]]):\
            The existing requests.
        resolver_to_synchronize (UriResolver): The URI resolver \
            to synchronize.
        options (Optional[RequestSynchronizerResolverOptions]):\
            The options to use.
    """

    __slots__ = ("resolver_to_synchronize", "options")

    existing_requests: Dict[Uri, Future[UriPackageOrWrapper]]
    resolver_to_synchronize: UriResolver
    options: Optional[RequestSynchronizerResolverOptions]

    def __init__(
        self,
        resolver_to_synchronize: UriResolver,
        options: Optional[RequestSynchronizerResolverOptions] = None,
    ):
        """Initialize a new RequestSynchronizerResolver instance.

        Args:
            resolver_to_synchronize (UriResolver): The URI resolver \
                to synchronize.
            options (Optional[RequestSynchronizerResolverOptions]):\
                The options to use.
        """
        self.resolver_to_synchronize = resolver_to_synchronize
        self.options = options

    def get_options(self) -> Union[RequestSynchronizerResolverOptions, None]:
        """Get the options.

        Returns:
            Union[RequestSynchronizerResolverOptions, None]:\
                The options or None.
        """
        return self.options

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        """Try to resolve the given uri to a wrap package, wrapper or uri.

        Synchronize requests to the same uri.\
        If a request is already in progress, it returns the future\
        of the existing request.\
        If a request is not in progress, it creates a new request\
        and returns the future of the new request.

        Args:
            uri (Uri): The uri to resolve.
            client (InvokerClient[UriPackageOrWrapper]): The client to use.
            resolution_context (IUriResolutionContext[UriPackageOrWrapper]):\
                The resolution context.

        Returns:
            UriPackageOrWrapper: The resolved uri package, wrapper or uri.
        """
        sub_context = resolution_context.create_sub_history_context()

        if existing_request := self.existing_requests.get(uri):
            uri_package_or_wrapper = await existing_request
            resolution_context.track_step(
                UriResolutionStep(
                    source_uri=uri,
                    result=uri_package_or_wrapper,
                    description="RequestSynchronizerResolver (Cache)",
                )
            )
            return uri_package_or_wrapper

        request_future = ensure_future(
            self.resolver_to_synchronize.try_resolve_uri(
                uri,
                client,
                sub_context,
            )
        )
        self.existing_requests[uri] = request_future
        uri_package_or_wrapper = await request_future
        resolution_context.track_step(
            UriResolutionStep(
                source_uri=uri,
                result=uri_package_or_wrapper,
                description="RequestSynchronizerResolver (Cache)",
            )
        )
        return uri_package_or_wrapper
