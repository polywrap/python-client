from ..python_client_config_builder import ClientConfigBuilder

print(ClientConfigBuilder)

def test_client_config_builder_adds_default_config():
    ClientConfigBuilder.add_defaults()
    pass

def test_client_config_builder():
    config = ClientConfigBuilder().add({})
    pass
