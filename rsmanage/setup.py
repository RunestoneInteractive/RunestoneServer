from setuptools import setup

setup(
    name="rsmanage",
    version="0.1",
    py_modules=["rsmanage"],
    install_requires=["click", "pgcli"],
    entry_points="""
        [console_scripts]
        rsmanage=rsmanage:cli
    """,
)
