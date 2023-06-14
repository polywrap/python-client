"""This module contains Error types for the polywrap-manifest package."""


class ManifestError(Exception):
    """Base class for all exceptions in this module."""


class DeserializeManifestError(ManifestError):
    """Raised when a manifest cannot be deserialized."""


__all__ = ["ManifestError", "DeserializeManifestError"]
