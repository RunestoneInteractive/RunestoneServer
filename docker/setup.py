# ******************************************************************
# |docname| - Provide `docker_tools.py` as the script `docker-tools`
# ******************************************************************
from setuptools import setup

setup(
    name="runestone-docker-tools",
    version="0.1",
    install_requires=["click", "click-web"],
    entry_points={
        "console_scripts": ["docker-tools = docker_tools:cli"]
    },
)
