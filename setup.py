# ----------------------------------------------------------------------------------------------------------------------
# - Package Imports -
# ----------------------------------------------------------------------------------------------------------------------
# General Packages
from __future__ import annotations
import setuptools

# Custom Library

# Custom Packages

# ----------------------------------------------------------------------------------------------------------------------
# - Code -
# ----------------------------------------------------------------------------------------------------------------------
def version_handler() -> str:
    version = 0,1,1
    version_str = ".".join(str(i) for i in version)

    with open("src/AthenaTwitchBot/_info/_v.py", "w") as file:
        file.write(f"def _version():\n    return '{version_str}'")

    return version_str

setuptools.setup(
    name="AthenaTwitchBot",
    version=version_handler(),
    author="Andreas Sas",
    author_email="",
    description="A Twitch bot Connector",
    url="https://github.com/DirectiveAthena/AthenaTwitchBot",
    project_urls={
        "Bug Tracker": "https://github.com/DirectiveAthena/AthenaTwitchBot/issues",
    },
    license="GPLv3",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "AthenaLib>=1.1.0",
        "AthenaColor>=6.0.1"
    ]
)