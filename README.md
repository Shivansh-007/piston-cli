# Piston CLI
[![](https://img.shields.io/github/license/Shivansh-007/piston-cli?style=for-the-badge)]()
[![](https://img.shields.io/github/issues/Shivansh-007/piston-cli?style=for-the-badge)]()
[![](https://img.shields.io/github/issues-pr/Shivansh-007/piston-cli?style=for-the-badge)]()
[![](https://img.shields.io/github/workflow/status/Shivansh-007/piston-cli/Linting/main?style=for-the-badge)]()

A cli tool which uses the [piston api](https://github.com/engineer-man/piston), developed by Engineerman and his team to compile over 35 languages instantly. Accepts files, paste.pythondiscord.com links and input.


### Commands
```bash
# Installing the package
pip3.8 install piston-cli -U
# Help Command
piston -h
```

### Languages
```bash
piston --list
```

## How to run it? (Contributing)
```shell
# This will install the development and project dependencies.
pipenv sync --dev

# This will install the pre-commit hooks.
pipenv run precommit

# Optionally: run pre-commit hooks to initialize them.
# You can start working on the feature after this.
pipenv run pre-commit run --all-files

# Run it
pipenv run start
```
