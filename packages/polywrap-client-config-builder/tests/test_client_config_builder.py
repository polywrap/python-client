from polywrap_client_config_builder import ClientConfigBuilder


def test_client_config_builder_adds_default_config():
    ClientConfigBuilder.add_defaults()
    pass



def test_client_config_builder_adds_config():
    config = ClientConfigBuilder().add({})
    pass

def test_client_config_builder_adds_uri_resolver():
    pass