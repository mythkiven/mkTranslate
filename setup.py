#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import re
from distutils.core import setup
from setuptools import setup, find_packages


def get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, 'rb') as f:
            return f.read().decode('utf8')
    except IOError:
        pass


def get_version():
    init_py = get_file(os.path.dirname(__file__), 'mkTranslation', '__init__.py')
    pattern = r"{0}\W*=\W*'([^']+)'".format('__version__')
    version, = re.findall(pattern, init_py)
    return version


def get_description():
    init_py = get_file(os.path.dirname(__file__), 'mkTranslation', '__init__.py')
    pattern = r'"""(.*?)"""'
    description, = re.findall(pattern, init_py, re.DOTALL)
    return description



def install():
    setup(
        name='mkTranslation',
        version=get_version(),
        description=get_description(),
        license='MIT',
        author='MythKiven',
        author_email='mythkiven' '@' 'qq.com',
        url='https://github.com/mythkiven/mkTranslate',
        packages=find_packages(exclude=['test']),
        keywords='google translate translator',
        install_requires=[
            'requests',
        ],
        extras_require={
            'h2': ['hyper'],
        },
        tests_require=[
            'pytest',
            'coveralls',
        ],
        scripts=['translate','trans'],
        console=['translate.exe']
    )


if __name__ == "__main__":
    install()
