import polywrap_fs_plugin

headline = polywrap_fs_plugin.__name__.replace("_", " ").title()
header = headline + "\n" + "=" * len(headline)
docstring = polywrap_fs_plugin.__doc__
docs = header + "\n" + docstring

with open("README.rst", "w") as f:
    f.write(docs)
