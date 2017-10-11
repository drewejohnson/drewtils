"""Setup for drewtils project."""

try:
    from setuptools import setup
    setupTools = True
except ImportError:
    from distutils.core import setup
    setupTools = False

_classifiers = [
    'License :: OSI Approved :: MIT License',
]

with open('pip_readme.rst') as readme:
    long_description = readme.read()

setupArgs = {
    'name': 'drewtils',
    'version': "0.1.7",
    'packages': ['drewtils'],
    'author': 'Andrew Johnson',
    'author_email': '1drew.e.johnson@gmail.com',
    'description': 'Simple tools to make testing and file parsing easier',
    'long_description': long_description,
    'license': 'MIT',
    'keywords': 'parsing files unittest testing',
    'url': 'https://github.com/drewejohnson/drewtils',
    'classifiers': _classifiers,
}

if setupTools:
    setupArgs.update(**{
        'test_suite': 'drewtils.tests',
        'python_requires': '>=2.7,!=3.1,!=3.2,!=3.3,!=3.4'
    })

setup(**setupArgs)