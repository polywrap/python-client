import polywrap_core

headline = polywrap_core.__name__.replace("_", " ").title()
header = headline + "\n" + "=" * len(headline)
docstring = polywrap_core.__doc__
docs = header + "\n" + docstring

with open("README.rst", "w") as f:
    f.write(docs)
