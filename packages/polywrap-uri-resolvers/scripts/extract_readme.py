import polywrap_uri_resolvers

headline = polywrap_uri_resolvers.__name__.replace("_", " ").title()
header = headline + "\n" + "=" * len(headline)
docstring = polywrap_uri_resolvers.__doc__
docs = header + "\n" + docstring

with open("README.rst", "w") as f:
    f.write(docs)
