
# Polywrap Python Client
## This object allows you to build proper Polywrapt ClientConfig objects

These objects are needed to configure your python client's wrappers, pluggins, env variables, resolvers and interfaces.

Look at [this file](./polywrap_client_config_builder/client_config_builder.py) to detail all of its functionality
And at [tests](./tests/test_client_config_builder.py)

---

The current implementation uses the `ClientConfig` as a dataclass to later create an Abstract Base Class of a `BaseClientConfigBuilder` which defines more clearly the functions of the module, like add_envs, set_resolvers, remove_wrappers, and so on.  

This `BaseClientConfigBuilder` is later used in the class `ClientConfigBuilder` which only implements the build method, for now, and inherits all the abstract methods of the `BaseClientConfigBuilder`.