from dataclasses import dataclass
from typing import Optional, cast
from polywrap_core import (
    IUriResolutionContext,
    InvokerClient,
    Uri,
    UriPackage,
    UriPackageOrWrapper,
    UriResolver,
    UriWrapper,
)
from polywrap_manifest import DeserializeManifestOptions

from ..abc import ResolverWithHistory
from ...types import UriResolutionStep


@dataclass(kw_only=True, slots=True)
class PackageToWrapperResolverOptions:
    deserialize_manifest_options: Optional[DeserializeManifestOptions]


class PackageToWrapperResolver(ResolverWithHistory):
    resolver: UriResolver
    options: Optional[PackageToWrapperResolverOptions]

    def __init__(
        self,
        resolver: UriResolver,
        options: Optional[PackageToWrapperResolverOptions] = None,
    ) -> None:
        self.resolver = resolver
        self.options = options

    async def _try_resolve_uri(
        self,
        uri: Uri,
        client: InvokerClient[UriPackageOrWrapper],
        resolution_context: IUriResolutionContext[UriPackageOrWrapper],
    ) -> UriPackageOrWrapper:
        sub_context = resolution_context.create_sub_context()
        result = await self.resolver.try_resolve_uri(uri, client, sub_context)
        if isinstance(result, UriPackage):
            wrapper = await cast(
                UriPackage[UriPackageOrWrapper], result
            ).package.create_wrapper()
            result = UriWrapper(uri, wrapper)

        resolution_context.track_step(
            UriResolutionStep(
                source_uri=uri,
                result=result,
                sub_history=sub_context.get_history(),
                description=self.get_step_description(),
            )
        )
        return result

    def get_step_description(self) -> str:
        return self.__class__.__name__
