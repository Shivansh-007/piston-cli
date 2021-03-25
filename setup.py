"""
This file is used to install this package via the pip tool.

It keeps track of versioning, as well as dependencies and
what versions of python we support.
"""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    README = readme_file.read()

setup_args = dict(
    name="piston-cli",
    version="1.3.0",
    description="A cli tool with an terminal editor to compile over "
    "35 languages instantly using the piston api.",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    author="Shivansh-007",
    keywords="piston compiler cli compile run",
    url="https://github.com/Shivansh-007/piston-cli",
    entry_points={
        "console_scripts": ["piston=piston:main"],
    },
)

install_requires = ["rich", "prompt-toolkit", "requests", "pygments"]

if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)
