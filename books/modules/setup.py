from distutils.core import setup

setup(
    name='runestone',
    version='0.1dev',
    packages=['luther','gatech','luther.sphinx','luther.sphinx.activecode'],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    scripts=['bin/runestone'],
    data_files=[('common',['common/*'])],
    long_description=open('README.txt').read(),
)