import polywrap_ethereum_provider

headline = polywrap_ethereum_provider.__name__.replace("_", " ").title()
header = headline + "\n" + "=" * len(headline)
docstring = polywrap_ethereum_provider.__doc__
docs = header + "\n" + docstring

with open("README.rst", "w") as f:
    f.write(docs)
