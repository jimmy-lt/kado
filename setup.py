# setup.py
# ========
#
# Copying
# -------
#
# Copyright (c) 2018 kado authors and contributors.
#
# This file is part of the *kado* project.
#
# kado is a free software project. You can redistribute it and/or
# modify if under the terms of the MIT License.
#
# This software project is distributed *as is*, WITHOUT WARRANTY OF ANY
# KIND; including but not limited to the WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE and NONINFRINGEMENT.
#
# You should have received a copy of the MIT License along with
# kado. If not, see <http://opensource.org/licenses/MIT>.
#
import os

from contextlib import suppress
from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))
LONG_DESCRIPTION = ''
with suppress(OSError), open(os.path.join(HERE, 'README.rst')) as fp:
    LONG_DESCRIPTION = fp.read()


setup(
    name='kado',
    version='0.0.0-alpha0',
    license='MIT',
    url='https://github.com/spack971/kado',

    author='Jimmy Thrasibule',
    author_email='kado@jimmy.lt',

    description='An object store.',
    long_description=LONG_DESCRIPTION,
    keywords='object-store',

    packages=find_packages(),

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers.
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 1 - Planning',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',

        'Natural Language :: English',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',

        'Operating System :: POSIX',

        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
    ],

    install_requires=[
        'semver',
        'xxhash',
    ],
)
