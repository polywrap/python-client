import polywrap_client

headline = polywrap_client.__name__.replace("_", " ").title()
header = headline + "\n" + "=" * len(headline)
docstring = polywrap_client.__doc__
docs = header + "\n" + docstring

with open("README.rst", "w") as f:
    f.write(docs)
