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
def readme_handler() -> str:
    with open("README.md", "r") as readme_file:
        return readme_file.read()

def version_handler() -> str:
    # ------------------------------------------------------------------------------------------------------------------
    version = 0,8,1 # <-- DEFINE THE VERSION IN A TUPLE FORMAT HERE
    # ------------------------------------------------------------------------------------------------------------------
    return ".".join(str(i) for i in version)

setuptools.setup(
    name="AthenaTwitchLib",
    version=version_handler(),
    author="Andreas Sas",
    author_email="",
    description="A library to create Twitch Chat Bots and connect to the Twitch Helix API.",
    long_description=readme_handler(),
    long_description_content_type="text/markdown",
    url="https://github.com/Athena-Chaos-Driven-Code/AthenaTwitchLib",
    project_urls={
        "Bug Tracker": "https://github.com/Athena-Chaos-Driven-Code/AthenaTwitchLib/issues",
    },
    license="GPLv3",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.11",
    install_requires=[
        "AthenaLib>=1.1.0",
        "AthenaColor>=6.0.1"
    ]
)
