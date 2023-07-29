"""This package contains the Filesystem plugin."""
import base64
import os
import shutil
import stat
from typing import Any

from polywrap_core import InvokerClient
from polywrap_plugin import PluginPackage

from .wrap import *


class FileSystemPlugin(Module[None]):
    """Defines the Filesystem plugin."""

    def read_file(
        self, args: ArgsReadFile, client: InvokerClient, env: None
    ) -> bytes:
        """Read a file from the filesystem and return its contents as bytes. """
        with open(args["path"], "rb") as f:
            return f.read()

    def read_file_as_string(
        self,
        args: ArgsReadFileAsString,
        client: InvokerClient,
        env: None,
    ) -> str:
        """Read a file from the filesystem, decode it using provided encoding\
            and return its contents as a string. """
        encoding = args.get("encoding", "utf-8")
        with open(args["path"], "rb") as f:
            content = f.read()

        if encoding == "ASCII":
            return content.decode("ascii")
        if encoding == "UTF8":
            return content.decode("utf-8")
        if encoding == "UTF16LE":
            return content.decode("utf-16-le")
        if encoding == "UCS2":
            return content.decode("utf-16")
        if encoding == "LATIN1":
            return content.decode("iso-8859-1")
        if encoding == "BINARY":
            return content.decode()
        if encoding == "BASE64":
            return base64.b64encode(content).decode("ascii")
        if encoding == "BASE64URL":
            return base64.urlsafe_b64encode(content).decode("ascii").rstrip("=")
        if encoding == "HEX":
            return content.hex()

        raise ValueError(f"Unsupported encoding: {encoding}")

    def exists(
        self, args: ArgsExists, client: InvokerClient, env: None
    ) -> bool:
        """Check if a file or directory exists."""
        return os.path.exists(args["path"])

    def write_file(
        self, args: ArgsWriteFile, client: InvokerClient, env: None
    ) -> bool:
        """Write data to a file on the filesystem."""
        with open(args["path"], "wb") as f:
            f.write(args["data"])
        return True


    def mkdir(self, args: ArgsMkdir, client: InvokerClient, env: None):
        """Create directories on the filesystem."""
        path = args["path"]
        if args.get("recursive", False):
            os.makedirs(path, exist_ok=True)
        else:
            parent_dir = os.path.dirname(path)
            if not os.path.exists(parent_dir):
                raise FileNotFoundError(f"Parent directory does not exist: {parent_dir}")
            os.mkdir(path)


    def rm(
        self, args: ArgsRm, client: InvokerClient, env: None
    ) -> bool:
        """Remove a file or directory from the filesystem."""
        if os.path.isdir(args["path"]):
            if args.get("force", False) and args.get("recursive", False):
                def force_remove(action: Any, name: str, exc: Exception) -> None:
                    os.chmod(name, stat.S_IWRITE)
                    os.remove(name)

                shutil.rmtree(args["path"], onerror=force_remove)
            elif args.get("recursive", False):
                shutil.rmtree(args["path"])
            else:
                os.rmdir(args["path"])
        else:
            os.remove(args["path"])
        return True

    def rmdir(
        self, args: ArgsRmdir, client: InvokerClient, env: None
    ) -> bool:
        """Remove an empty directory from the filesystem."""
        os.rmdir(args["path"])
        return True


def file_system_plugin() -> PluginPackage[None]:
    """Create a Polywrap plugin instance for interacting with EVM networks."""
    return PluginPackage(
        module=FileSystemPlugin(None), manifest=manifest
    )
