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
"""Test classes for pynamedotcom."""


from __future__ import print_function
from __future__ import unicode_literals

import json
import os
import pytest

from pynamedotcom import API
from pynamedotcom.domain import Domain


@pytest.fixture
def api():
    """Create test API instance."""
    host = "api.dev.name.com"
    path = os.path.join(os.path.dirname(__file__), "auth.json")
    with open(path) as f:
        auth = json.load(f)

    def func():
        return API(host=host, **auth)

    return func


class TestAPI(object):
    """Test cases."""

    def test_ping(self, api):
        """Test ping() method."""
        with api() as api:
            api.ping()

    def test_get_domain(self, api):
        """Test get_domain() method."""
        with api() as api:
            name = "maddison.family"
            domain = api.get_domain(name=name)
            assert isinstance(domain, Domain)
            assert domain.name == name
            assert isinstance(domain.renewal_price, float)

    def test_get_domains(self, api):
        """Test domains retrieval."""
        with api() as api:
            for domain in api.domains:
                assert isinstance(domain, Domain)
                assert isinstance(domain.renewal_price, float)
