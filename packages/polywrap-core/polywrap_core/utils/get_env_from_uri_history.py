from typing import Any, Dict, List, Union

from ..types import Client, Uri


def get_env_from_uri_history(
    uri_history: List[Uri], client: Client
) -> Union[Dict[str, Any], None]:
    for uri in uri_history:
        return client.get_env_by_uri(uri)
