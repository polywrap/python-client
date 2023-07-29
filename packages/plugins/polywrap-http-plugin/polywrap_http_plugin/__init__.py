"""This package contains the HTTP plugin."""
import base64
from typing import List, Optional, cast

from httpx import Client
from httpx import Response as HttpxResponse
from httpx._types import RequestFiles
from polywrap_core import InvokerClient
from polywrap_msgpack import GenericMap
from polywrap_plugin import PluginPackage

from .wrap import (
    ArgsGet,
    ArgsPost,
    FormDataEntry,
    Module,
    Response,
    ResponseType,
    manifest,
)


def _is_response_binary(args: ArgsGet) -> bool:
    if args.get("request") is None:
        return False
    if not args["request"]:
        return False
    if not args["request"].get("responseType"):
        return False
    if args["request"]["responseType"] == 1:
        return True
    if args["request"]["responseType"] == "BINARY":
        return True
    return args["request"]["responseType"] == ResponseType.BINARY


class HttpPlugin(Module[None]):
    """HTTP plugin."""

    def __init__(self):
        """Initialize the HTTP plugin."""
        super().__init__(None)
        self.client = Client()

    def get(
        self, args: ArgsGet, client: InvokerClient, env: None
    ) -> Optional[Response]:
        """Make a GET request to the given URL."""
        res: HttpxResponse
        if args.get("request") is None:
            res = self.client.get(args["url"], follow_redirects=True)
        elif args["request"] is not None:
            res = self.client.get(
                args["url"],
                params=args["request"].get("urlParams"),
                headers=args["request"].get("headers"),
                timeout=cast(float, args["request"].get("timeout")),
                follow_redirects=True,
            )
        else:
            res = self.client.get(args["url"], follow_redirects=True)

        if _is_response_binary(args):
            return Response(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=GenericMap(dict(res.headers)),
                body=base64.b64encode(res.content).decode(),
            )

        return Response(
            status=res.status_code,
            statusText=res.reason_phrase,
            headers=GenericMap(dict(res.headers)),
            body=res.text,
        )

    def post(
        self, args: ArgsPost, client: InvokerClient, env: None
    ) -> Optional[Response]:
        """Make a POST request to the given URL."""
        res: HttpxResponse
        if args.get("request") is None:
            res = self.client.post(args["url"], follow_redirects=True)
        elif args["request"] is not None:
            content = (
                args["request"]["body"].encode()
                if args["request"]["body"] is not None
                else None
            )

            files = self._get_files_from_form_data(
                args["request"].get("formData") or []
            )

            if args["request"].get("headers"):
                headers = cast(GenericMap[str, str], args["request"]["headers"])
                if headers["Content-Type"] == "multipart/form-data":
                    # Let httpx handle the content type if it's multipart/form-data
                    # because it will automatically generate the boundary.
                    del headers["Content-Type"]

            res = self.client.post(
                args["url"],
                content=content,
                files=files,
                params=args["request"].get("urlParams"),
                headers=args["request"].get("headers"),
                timeout=cast(float, args["request"].get("timeout")),
                follow_redirects=True,
            )

        else:
            res = self.client.post(args["url"], follow_redirects=True)

        if _is_response_binary(args):
            return Response(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=GenericMap(dict(res.headers)),
                body=base64.b64encode(res.content).decode(),
            )

        return Response(
            status=res.status_code,
            statusText=res.reason_phrase,
            headers=GenericMap(dict(res.headers)),
            body=res.text,
        )

    def _get_files_from_form_data(self, form_data: List[FormDataEntry]) -> RequestFiles:
        files: RequestFiles = {}
        for entry in form_data:
            file_content = cast(str, entry["value"]) if entry.get("value") else ""
            if entry.get("type"):
                file_content = (
                    base64.b64decode(cast(str, entry["value"]).encode())
                    if entry.get("value")
                    else bytes()
                )
            files[entry["name"]] = file_content
        return files


def http_plugin():
    """Factory function for the HTTP plugin."""
    return PluginPackage(module=HttpPlugin(), manifest=manifest)
