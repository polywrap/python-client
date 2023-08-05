import polywrap_client_config_builder

headline = polywrap_client_config_builder.__name__.replace("_", " ").title()
header = headline + "\n" + "=" * len(headline)
docstring = polywrap_client_config_builder.__doc__
docs = header + "\n" + docstring

with open("README.rst", "w") as f:
    f.write(docs)
