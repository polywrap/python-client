"""This module contains an utility function for building a clean history of URI resolution steps."""
import traceback
from typing import List, Optional, Union

from ..types import IUriResolutionStep, WrapPackage, Uri

CleanResolutionStep = List[Union[str, "CleanResolutionStep"]]


def build_clean_uri_history(
    history: List[IUriResolutionStep], depth: Optional[int] = None
) -> CleanResolutionStep:
    """Build a clean history of the URI resolution steps.

    Args:
        history: A list of URI resolution steps.
        depth: The depth of the history to build.

    Returns:
        CleanResolutionStep: A clean history of the URI resolution steps.
    """
    clean_history: CleanResolutionStep = []

    if depth is not None:
        depth -= 1

    if not history:
        return clean_history

    for step in history:
        clean_history.append(_build_clean_history_step(step))

        if (
            not step.sub_history
            or len(step.sub_history) == 0
            or (depth is not None and depth < 0)
        ):
            continue

        sub_history = build_clean_uri_history(step.sub_history, depth)
        if len(sub_history) > 0:
            clean_history.append(sub_history)

    return clean_history


def _build_clean_history_step(step: IUriResolutionStep) -> str:
    if step.result.is_err():
        formatted_exc = traceback.format_tb(step.result.unwrap_err().__traceback__)
        return (
            f"{step.source_uri} => {step.description} => error ({''.join(formatted_exc)})"
            if step.description
            else f"{step.source_uri} => error ({''.join(formatted_exc)})"
        )

    uri_package_or_wrapper = step.result.unwrap()

    if isinstance(uri_package_or_wrapper, Uri):
        if step.source_uri == uri_package_or_wrapper:
            return (
                f"{step.source_uri} => {step.description}"
                if step.description
                else f"{step.source_uri}"
            )
        return (
            f"{step.source_uri} => {step.description} => uri ({uri_package_or_wrapper.uri})"
            if step.description
            else f"{step.source_uri} => uri ({uri_package_or_wrapper})"
        )
    if isinstance(uri_package_or_wrapper, WrapPackage):
        return (
            f"{step.source_uri} => {step.description} => package ({uri_package_or_wrapper})"
            if step.description
            else f"{step.source_uri} => package ({uri_package_or_wrapper})"
        )
    return (
        f"{step.source_uri} => {step.description} => wrapper ({uri_package_or_wrapper})"
        if step.description
        else f"{step.source_uri} => wrapper ({uri_package_or_wrapper})"
    )