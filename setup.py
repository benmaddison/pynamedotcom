#!/usr/bin/env python
# Copyright (c) 2018 Ben Maddison. All rights reserved.
#
# The contents of this file are licensed under the MIT License
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Setup configuration script for pynamedotcom."""

from __future__ import print_function
from __future__ import unicode_literals

from setuptools import find_packages, setup

descr = "A python library to interact with the name.com api."

with open('packaging/VERSION') as f:
    version = f.read().strip()
with open('packaging/requirements.txt') as f:
    requirements = f.read().split("\n")

try:
    import pypandoc
    readme = pypandoc.convert_file('README.md', 'rst', format='md')
except (ImportError, RuntimeError) as e:
    print("README conversion failed: {}".format(e))
    readme = None


setup(
    name='pynamedotcom',
    version=version,
    author='Ben Maddison',
    author_email='benm@workonkonline.co.za',
    description=descr,
    long_description=readme,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
    ],
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/benmaddison/pynamedotcom',
    download_url='https://github.com/benmaddison/pynamedotcom/%s' % version,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'namedotcom=pynamedotcom.cli:main',
        ]
    }
)
