import polywrap_wasm

headline = polywrap_wasm.__name__.replace("_", " ").title()
header = headline + "\n" + "=" * len(headline)
docstring = polywrap_wasm.__doc__
docs = header + "\n" + docstring

with open("README.rst", "w") as f:
    f.write(docs)
