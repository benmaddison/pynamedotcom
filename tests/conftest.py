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
"""Fixtures for pynamedotcom tests."""


from __future__ import print_function
from __future__ import unicode_literals

import json
import os
import pytest

from pynamedotcom import API


@pytest.fixture(scope="session")
def api():
    """Create test API instance."""
    host = "api.dev.name.com"
    path = os.path.join(os.path.dirname(__file__), "auth.json")
    with open(path) as f:
        auth = json.load(f)

    def func():
        return API(host=host, **auth)

    return func


@pytest.fixture(scope="session")
def domain(api):
    """Create test Domain instance."""
    name = "maddison.family"
    with api() as api:
        domain = api.domain(name=name)
    return domain
