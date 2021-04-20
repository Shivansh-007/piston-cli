import tomlkit


def get_project_version() -> str:
    """Set version only in toml file and get it wherever you want."""
    with open("pyproject.toml") as pyproject:
        file_contents = pyproject.read()

    return str(tomlkit.parse(file_contents)["tool"]["poetry"]["version"])
