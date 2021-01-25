# Piston CLI
A cli tool which uses the piston api, developed by Engineerman and his team to compile over 20 languages instantly, Accepts files, paste.pythondiscord.com links and input.

## How to run it?
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

### Commands
```bash
pipenv run start -h
```

### Languages
```bash
pipenv run start -l
```
