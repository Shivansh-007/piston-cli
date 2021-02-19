from pathlib import Path

import yaml


def load_languages() -> dict:
    """Loads languages from the yml file containing the language and its aliases."""
    with open(Path("piston/utilities/languages.yml"), "r") as stream:
        languages = yaml.safe_load(stream)
    return languages


def all_languages() -> dict:
    """Returns all the languages along with its alis in a nice dict lang: alias."""
    languages = load_languages()
    languages = {lang: aliases for d in languages for lang, aliases in d.items()}
    return languages
