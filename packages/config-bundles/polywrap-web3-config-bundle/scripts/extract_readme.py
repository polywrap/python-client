import polywrap_web3_config_bundle

headline = polywrap_web3_config_bundle.__name__.replace("_", " ").title()
header = headline + "\n" + "=" * len(headline)
docstring = polywrap_web3_config_bundle.__doc__
docs = header + "\n" + docstring

with open("README.rst", "w") as f:
    f.write(docs)
