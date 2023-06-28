from polywrap_core import (
    CleanResolutionStep,
    Uri,
    build_clean_uri_history,
    UriResolutionStep,
)
import pytest


@pytest.fixture
def history() -> list[UriResolutionStep]:
    return [
        UriResolutionStep(
            source_uri=Uri.from_str("test/1"),
            result=Uri.from_str("test/2"),
            description="AggreagatorResolver",
            sub_history=[
                UriResolutionStep(
                    source_uri=Uri.from_str("test/1"),
                    result=Uri.from_str("test/2"),
                    description="ExtensionRedirectResolver",
                ),
            ],
        ),
        UriResolutionStep(
            source_uri=Uri.from_str("test/2"),
            result=Uri.from_str("test/3"),
            description="SimpleRedirectResolver",
        ),
    ]


@pytest.fixture
def expected() -> CleanResolutionStep:
    return [
        "wrap://test/1 => AggreagatorResolver => uri (wrap://test/2)",
        ["wrap://test/1 => ExtensionRedirectResolver => uri (wrap://test/2)"],
        "wrap://test/2 => SimpleRedirectResolver => uri (wrap://test/3)",
    ]


def test_build_clean_uri_history(
    history: list[UriResolutionStep], expected: CleanResolutionStep
):
    print(build_clean_uri_history(history))
    assert build_clean_uri_history(history) == expected
