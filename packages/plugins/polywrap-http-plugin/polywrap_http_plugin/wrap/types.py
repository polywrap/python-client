# NOTE: This is an auto-generated file. All modifications will be overwritten.
# type: ignore
from __future__ import annotations

from typing import TypedDict, Optional
from enum import IntEnum

from polywrap_core import InvokerClient, Uri
from polywrap_msgpack import GenericMap


### Env START ###

### Env END ###

### Objects START ###

Response = TypedDict("Response", {
    "status": int,
    "statusText": str,
    "headers": Optional[GenericMap[str, str]],
    "body": Optional[str],
})

Request = TypedDict("Request", {
    "headers": Optional[GenericMap[str, str]],
    "urlParams": Optional[GenericMap[str, str]],
    "responseType": "ResponseType",
    "body": Optional[str],
    "formData": Optional[list["FormDataEntry"]],
    "timeout": Optional[int],
})

FormDataEntry = TypedDict("FormDataEntry", {
    "name": str,
    "value": Optional[str],
    "fileName": Optional[str],
    "type": Optional[str],
})

### Objects END ###

### Enums START ###
class ResponseType(IntEnum):
    TEXT = 0, "0", "TEXT"
    BINARY = 1, "1", "BINARY"

    def __new__(cls, value: int, *aliases: str):
        obj = int.__new__(cls)
        obj._value_ = value
        for alias in aliases:
            cls._value2member_map_[alias] = obj
        return obj

### Enums END ###

### Imported Objects START ###

### Imported Objects END ###

### Imported Enums START ###


### Imported Enums END ###

### Imported Modules START ###

### Imported Modules END ###

### Interface START ###


### Interface END ###
