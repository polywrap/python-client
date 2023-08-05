import polywrap_test_cases

headline = polywrap_test_cases.__name__.replace("_", " ").title()
header = headline + "\n" + "=" * len(headline)
docstring = polywrap_test_cases.__doc__
docs = header + "\n" + docstring

with open("README.rst", "w") as f:
    f.write(docs)
