# -*- coding: utf-8 -*-

try:
    import logging
    import multiprocessing
except:
    pass

import sys
py_version = sys.version_info[:2]

try:
    from setuptools import setup, find_packages
except ImportError:
    from setuptools import setup, find_packages

packages = [
    'spell_checker'
]

requires = []

test_requirements = []
setup(
    name='farsi_spell_checker',
    version='0.0.1a',
    description='Persian Spell_Checker in Python',
    author='eteamin',
    author_email='aminetesamian1371@gmail.com',
    url='https://github.com/eteamin/spell_checker',
    packages=packages,
    install_requires=requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=test_requirements,

)
