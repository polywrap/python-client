"""This module contains the get_uri_resolution_path function."""
from typing import List

from polywrap_core import UriResolutionStep


def get_uri_resolution_path(
    history: List[UriResolutionStep],
) -> List[UriResolutionStep]:
    """Get the URI resolution path from the URI resolution history.

    Args:
        history (List[UriResolutionStep]): URI resolution history

    Returns:
        List[UriResolutionStep]: URI resolution path
    """
    # Get all non-empty items from the resolution history

    def add_uri_resolution_path_for_sub_history(
        step: UriResolutionStep,
    ) -> UriResolutionStep:
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
