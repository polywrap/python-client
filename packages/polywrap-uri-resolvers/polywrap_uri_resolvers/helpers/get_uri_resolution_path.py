from typing import List

from polywrap_core import IUriResolutionStep, IWrapPackage, Uri, Wrapper


def get_uri_resolution_path(
    history: List[IUriResolutionStep],
) -> List[IUriResolutionStep]:
    # Get all non-empty items from the resolution history

    def add_uri_resolution_path_for_sub_history(
        step: IUriResolutionStep,
    ) -> IUriResolutionStep:
        if step.sub_history and len(step.sub_history):
            step.sub_history = get_uri_resolution_path(step.sub_history)
        return step

    return [
        add_uri_resolution_path_for_sub_history(step)
        for step in filter(
            lambda step: step.result.is_err()
            or (
                isinstance(step.result.unwrap(), Uri)
                and step.result.unwrap() != step.source_uri
            )
            or isinstance(step.result.unwrap(), (IWrapPackage, Wrapper)),
            history,
        )
    ]
