import polywrap_manifest

headline = polywrap_manifest.__name__.replace("_", " ").title()
header = headline + "\n" + "=" * len(headline)
docstring = polywrap_manifest.__doc__
docs = header + "\n" + docstring

with open("README.rst", "w") as f:
    f.write(docs)
