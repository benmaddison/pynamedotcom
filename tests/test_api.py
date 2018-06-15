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
import pynamedotcom
import pynamedotcom.domain
import pytest


@pytest.fixture
def auth():
    """Read test api credentials from file."""
    path = os.path.join(os.path.dirname(__file__), "auth.json")
    with open(path) as f:
        return json.load(f)


class TestAPI(object):
    """Test cases."""

    host = "api.dev.name.com"

    def test_ping(self, auth):
        """Test API ping."""
        with pynamedotcom.API(host=self.host, **auth) as api:
            api.ping()

    def test_get_domains(self, auth):
        """Test domains retrieval."""
        with pynamedotcom.API(host=self.host, **auth) as api:
            for domain in api.domains:
                assert isinstance(domain, pynamedotcom.domain.Domain)
