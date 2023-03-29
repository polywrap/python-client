from asyncio import Future, ensure_future
from typing import Any, Optional

from polywrap_core import (
    Dict,
    InvokerClient,
    IUriResolutionContext,
    UriResolver,
    Uri,
    UriPackageOrWrapper,
)

from ...types import UriResolutionStep


class RequestSynchronizerResolverOptions:
    should_ignore_cache: Optional[bool]


class RequestSynchronizerResolver(UriResolver):
    __slots__ = ("resolver_to_synchronize", "options")

    existing_requests: Dict[Uri, Future[UriPackageOrWrapper]]
    resolver_to_synchronize: UriResolver
    options: Optional[RequestSynchronizerResolverOptions]

    def __init__(
        self,
        resolver_to_synchronize: UriResolver,
        options: Optional[RequestSynchronizerResolverOptions],
    ):
        self.resolver_to_synchronize = resolver_to_synchronize
        self.options = options

    def get_options(self) -> Any:
        return self.options

    async def try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
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
