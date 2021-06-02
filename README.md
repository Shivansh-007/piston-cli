# Piston CLI

[![](https://img.shields.io/github/license/Shivansh-007/piston-cli?style=for-the-badge)]()
[![](https://img.shields.io/github/issues/Shivansh-007/piston-cli?style=for-the-badge)]()
[![](https://img.shields.io/github/workflow/status/Shivansh-007/piston-cli/Linting/main?style=for-the-badge)]()
[![](https://img.shields.io/pypi/pyversions/piston-cli?style=for-the-badge)]()
[![](https://img.shields.io/pypi/v/piston-cli?style=for-the-badge)]()
[![built with nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)

A cli tool which uses the [piston api](https://github.com/engineer-man/piston), developed by Engineerman and his team to compile over 35 languages instantly. Accepts files, paste.pythondiscord.com links and input.

### Installation

#### With pip

```bash
# Installing the package
pip install piston-cli -U
# Help Command
piston -h
```
#### With Nix/NixOS

`piston-cli` is available in [nixpkgs](https://github.com/nixos/nixpkgs) through the unstable channels.

You can install it with `nix-env`, or in a declarative way with configuration.nix or similar.

##### Flake support

`piston-cli` is a flake, that means you can easily add it to your flake based configuration:
Disclaimer: this also means you're using the development version, you could encounter bugs. If you want to use the stable version, install it from nixpkgs.

```nix
{
	inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
	inputs.piston-cli.url = "github:piston-cli/piston-cli";

	outputs = { nixpkgs, piston-cli }:
	let
		pkgs = import nixpkgs { system = "x86_64-linux"; overlays = [ piston-cli.overlay ]; };
	in
	 {
		 # use pkgs.piston-cli-unstable here
	 };
}
```

#### For Arch/ArchBased
##### With yay
```bash
yay piston-cli
```
##### With paru
```bash
paru piston-cli
```

Or any AUR helper you use with doesn't matter. You get the point.

### Example usage

#### Default

![example usage](media/piston-cli.png)

#### Shell

![example shell usage](media/piston-cli-shell.png)

#### File

![example file usage](media/piston-cli-file.png)

#### Link

![example link usage](media/piston-cli-link.png)

### Languages

```bash
piston --list
```

## How to run it? (Contributing)

```shell
# This will install the development and project dependencies.
poetry install

# This will install the pre-commit hooks.
poetry run task precommit

# Optionally: run pre-commit hooks to initialize them.
# You can start working on the feature after this.
poetry run task pre-commit run --all-files

# Run it
poetry run task start --help
```

## Contributing

You can comment on the issues you would like to work on.
