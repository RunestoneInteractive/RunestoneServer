from setuptools import setup

setup(
    name="rsmanage",
    version="1.0.0",
    py_modules=["rsmanage"],
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        rsmanage=rsmanage.rsmanage:cli
    """,
)
