#!/usr/bin/env python3
"""
Brew Formula Generator For Piston-CLI.

Generate Ruby code with URLs and file hashes for packages from PyPi
(i.e., piston-cli itself as well as its dependencies) to be included
in the Homebrew formula after a new release of piston-cli has been published
on PyPi.

<https://github.com/Homebrew/homebrew-core/blob/master/Formula/piston-cli.rb>
"""

import hashlib
import typing as t

import requests


VERSIONS = {
    # By default, we use the latest packages. But sometimes Requests has a maximum supported versions.
    # Take a look here before making a release: <https://github.com/psf/requests/blob/master/setup.py>
    "idna": "2.10",
}

DESCRIPTION = "Universal shell supporting code highlighting, files, and interpretation."

PACKAGES = (
    "piston-cli",
    "wcwidth",
    "urllib3",
    "typing-extensions",
    "rich",
    "requests",
    "Pygments",
    "prompt-toolkit",
    "idna",
    "commonmark",
    "colorama",
    "chardet",
    "certifi",
    "more-itertools",
    "PyYAML",
)


def get_package_meta(package_name: str) -> t.Optional[dict]:
    """Get package meta for a `package_name`."""
    api_url = f"https://pypi.org/pypi/{package_name}/json"
    resp = requests.get(api_url).json()
    hasher = hashlib.sha256()
    version = VERSIONS.get(package_name)
    if package_name not in VERSIONS:
        # Latest version
        release_bundle = resp["urls"]
    else:
        release_bundle = resp["releases"][version]

    for release in release_bundle:
        download_url = release["url"]
        if download_url.endswith(".tar.gz"):
            hasher.update(requests.get(download_url).content)
            return {
                "name": package_name,
                "url": download_url,
                "sha256": hasher.hexdigest(),
            }
    else:
        raise RuntimeError(f"{package_name}: download not found: {resp}")


def main() -> None:
    """Main script to print piston-cli homebrew formula."""
    package_meta_map = {
        package_name: get_package_meta(package_name) for package_name in PACKAGES
    }
    httpie_meta = package_meta_map.pop("piston-cli")

    print("class PistonCli < Formula")
    print("  include Language::Python::Virtualenv")

    # area: meta
    print()
    print(f'  desc "{DESCRIPTION}"')
    print('  homepage "https://github.com/Shivansh-007/piston-cli"')
    print('  url "{url}"'.format(url=httpie_meta["url"]))
    print('  sha256 "{sha256}"'.format(sha256=httpie_meta["sha256"]))
    print('  license "MIT"')
    print('\n  depends_on "python@3.9"')

    # area: deps
    print()
    for dep_meta in package_meta_map.values():
        print('  resource "{name}" do'.format(name=dep_meta["name"]))
        print('    url "{url}"'.format(url=dep_meta["url"]))
        print('    sha256 "{sha256}"'.format(sha256=dep_meta["sha256"]))
        print("  end")
        print("")

    # area: install
    print("  def install")
    print("    virtualenv_install_with_resources")
    print("  end")

    # add tests
    print()
    print("  test do")
    print('    assert_match "1.4.2", shell_output("#{bin}/piston --version")')
    print("  end")

    print("end")


if __name__ == "__main__":
    main()
