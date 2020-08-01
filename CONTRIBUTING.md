# Contributing

Thank you for considering to contribute to this project!

The following is a set of guidelines and resources for contributing to Auraxium.

## Coding Style

- Follow the official Python style guide [PEP 8](https://www.python.org/dev/peps/pep-0008/)

- Type hint your code according to [PEP 484](https://www.python.org/dev/peps/pep-0484/).

    You **must** annotate any public members (e.g. method arguments, return values or attribute types).

    It is also recommended to annotate any internal generics to help with catching errors, as well as to make it easier for others to understand your code.

    Finally, use the **broadest applicable** generic type for your arguments, i.e. the least restrictive protocol.

    > **Example:** If your function only has to iterate over the argument, use `Iterable`. If it also has to access its members by index, use `Sequence`.
    >
    > Only use the more restrictive type `List` if you require list-specific methods like `.append()` or `.clear()`.

    Refer to the [Mypy docs](https://mypy.readthedocs.io/en/stable/protocols.html#protocol-types) for more information.

- This project uses the [Google format](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) for its docstrings. Make sure the source code version is easy on the eye; don't get carried away with the ReST directives.

    Do not include type information in your docstrings as this information can be inferred via the type hints as well.

## Documentation

This project is documented in three places:

- Every public class or method must be documented in **the source code** via docstrings.

- Release-specific documentation, such as the public API, is dynamically generated from the source code and hosted on [Read the Docs](https://auraxium.readthedocs.io/en/latest/).

- Release-agnostic documentation, like guides, tutorials and references, live in the [GitHub Wiki](https://github.com/leonhard-s/auraxium/wiki) instead.

## Testing

This project uses the [`unittest` testing framework](https://docs.python.org/3/library/unittest.html) for code validation.

Currently, only the `auraxium.census` module is being tested at all, but higher coverage is always desirable.

## Environment

Feel free to add development tools to the `tools/` directory, or any form of editor-specific settings to the respective subfolder (e.g. `.vscode/`) to help other contributors get started.

Just make sure your tools are themselves well-documented, easy to use and provide some utility to other users.
