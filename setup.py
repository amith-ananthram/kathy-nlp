from setuptools import setup

setup(
    name='kathy-nlp',
    url='https://github.com/amith-ananthram/kathy-nlp',
    author='Kathy McKeown\'s NLP Lab',
    author_email='jladan@uwaterloo.ca',
    packages=['monitoring', 'profiling'],
    install_requires=['python-dateutil'],
    version='0.1',
    license='MIT',
    description='A collection of Python utilities for NLP research.',
    long_description=open('README.md').read()
)