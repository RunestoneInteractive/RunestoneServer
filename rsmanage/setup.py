from setuptools import setup

setup(
    name='rsmanage',
    version='0.1',
    py_modules=['rsmanager'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        rsmanage=rsmanager:cli
    ''',
)
