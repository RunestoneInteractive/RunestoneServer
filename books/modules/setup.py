from setuptools import setup, find_packages

setup(
    name='runestone',
    version='0.1dev',
    author = 'Brad Miller',
    author_email = 'bonelake@mac.com',
    packages= find_packages(),
    include_package_data = True,
    package_dir = {'' : '.'},
    package_data = { '' : ['js/*.js', 'css/*.css', '*.txt']},
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    scripts=['bin/runestone'],
    data_files=[('common',['common/*'])],
    long_description=open('README.txt').read(),
)