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
"""Setup configuration script for package."""

from __future__ import print_function
from __future__ import unicode_literals

import os
import re

from setuptools import find_packages, setup

package = {"__name__": find_packages()[0]}
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, package["__name__"], "__meta__.py")) as f:
    exec(f.read(), package)

with open(os.path.join(here, "packaging", "requirements.txt")) as f:
    package["__requirements__"] = f.readlines()

with open(os.path.join(here, "README.md")) as f:
    for line in f:
        match = re.match(r'<!--description: () -->', line)
        if match is not None:
            package["__description__"] = match.group(1)
            break
    else:
        package["__description__"] = None

try:
    import pypandoc
    package["__readme__"] = pypandoc.convert_file('README.md',
                                                  'rst', format='md')
except (ImportError, RuntimeError) as e:
    print("README conversion failed: {}".format(e))
    package["__readme__"] = None


setup(
    name=package["__name__"],
    version=package["__version__"],
    author=package["__author__"],
    author_email=package["__author_email__"],
    description=package["__description__"],
    long_description=package["__readme__"],
    license=package["__licence__"],
    classifiers=package["__classifiers__"],
    packages=find_packages(),
    include_package_data=True,
    url=package["__url__"],
    download_url="{}/{}".format(package["__url__"], package["__version__"]),
    install_requires=package["__requirements__"],
    entry_points=package["__entry_points__"]
)
