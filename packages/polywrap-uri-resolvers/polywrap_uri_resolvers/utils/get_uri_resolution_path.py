"""This module contains the get_uri_resolution_path function."""
from typing import List, TypeVar

from polywrap_core import IUriResolutionStep, UriLike

TUriLike = TypeVar("TUriLike", bound=UriLike)


def get_uri_resolution_path(
    history: List[IUriResolutionStep[TUriLike]],
) -> List[IUriResolutionStep[TUriLike]]:
    """Get the URI resolution path from the URI resolution history.

    Args:
        history (List[IUriResolutionStep[TUriLike]]): URI resolution history

    Returns:
        List[IUriResolutionStep[TUriLike]]: URI resolution path
    """
    # Get all non-empty items from the resolution history

    def add_uri_resolution_path_for_sub_history(
        step: IUriResolutionStep[TUriLike],
    ) -> IUriResolutionStep[TUriLike]:
        if step.sub_history and len(step.sub_history):
            step.sub_history = get_uri_resolution_path(step.sub_history)
        return step

    return [
        add_uri_resolution_path_for_sub_history(step)
        for step in filter(
            lambda step: step.source_uri != step.result,
            history,
        )
    ]
