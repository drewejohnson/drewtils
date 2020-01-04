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

with open('README.rst') as readme:
    long_description = readme.read()

setupArgs = {
    'name': 'drewtils',
    'version': "0.2.0",
    'packages': ['drewtils'],
    'author': 'Andrew Johnson',
    'author_email': 'drewej@protonmail.com',
    'description': 'Simple tools to make testing and file parsing easier',
    'long_description': long_description,
    'license': 'MIT',
    'keywords': 'parsing files',
    'url': 'https://github.com/drewejohnson/drewtils',
    'classifiers': _classifiers,
}

if setupTools:
    setupArgs.update(**{
        'test_suite': 'drewtils.tests',
        'python_requires': '>=3.5'
    })

setup(**setupArgs)
