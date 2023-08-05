import polywrap_msgpack

headline = polywrap_msgpack.__name__.replace("_", " ").title()
header = headline + "\n" + "=" * len(headline)
docstring = polywrap_msgpack.__doc__
docs = header + "\n" + docstring

with open("README.rst", "w") as f:
    f.write(docs)
