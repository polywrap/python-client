from typing import List, Union, Dict, Any

from ..types import CoreClient, Env, Uri


def get_env_from_uri_history(
    uri_history: List[Uri], client: CoreClient
) -> Union[Dict[str, Any], None]:
    for uri in uri_history:
        return client.get_env_by_uri(uri)
