from typing import List, Optional, Union

from ..types import IUriResolutionStep


CleanResolutionStep = List[Union[str, "CleanResolutionStep"]]


def build_clean_uri_history(
    history: List[IUriResolutionStep], depth: Optional[int] = ...
) -> CleanResolutionStep:
    ...


def _build_clean_history_step(step: IUriResolutionStep) -> str:
    ...