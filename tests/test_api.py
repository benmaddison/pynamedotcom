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
from pynamedotcom.contact import Contact, ROLES
from pynamedotcom.domain import Domain
from pynamedotcom.exceptions import DomainUnlockTimeError
from pynamedotcom.search import SearchResult


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


@pytest.fixture
def domain(api):
    """Create test Domain instance."""
    name = "maddison.family"
    with api() as api:
        domain = api.domain(name=name)
    return domain


class TestAPI(object):
    """API test cases."""

    def test_ping(self, api):
        """Test ping() method."""
        with api() as api:
            api.ping()

    def test_get_domain(self, api):
        """Test domain retrieval."""
        with api() as api:
            name = "maddison.family"
            domain = api.domain(name=name)
            assert isinstance(domain, Domain)
            assert domain.name == name
            assert isinstance(domain.renewal_price, float)
            with pytest.raises(AttributeError):
                domain.not_a_property
            for role, contact in domain.contacts.items():
                assert role in ROLES
                assert isinstance(contact, Contact)
                with pytest.raises(AttributeError):
                    contact.not_a_property

    def test_get_domains(self, api):
        """Test domains retrieval."""
        with api() as api:
            for domain in api.domains:
                assert isinstance(domain, Domain)
                assert isinstance(domain.renewal_price, float)

    def test_search_available(self, api):
        """Test successful availablility search."""
        with api() as api:
            name = "maddison.name"
            result = api.check_availability(name=name)
            assert isinstance(result, SearchResult)
            assert result.name == name
            assert result.purchasable
            with pytest.raises(AttributeError):
                result.not_a_property

    def test_search_unavailable(self, api):
        """Test unsuccessful availablility search."""
        with api() as api:
            name = "maddison.family"
            result = api.check_availability(name=name)
            assert isinstance(result, SearchResult)
            assert result.name == name
            assert not result.purchasable
            with pytest.raises(AttributeError):
                result.not_a_property


class TestDomain(object):
    """Domain test cases."""

    name = "maddison.family"

    def test_name_property(self, domain):
        """Test name getter."""
        assert domain.name == self.name

    def test_locked_property(self, domain):
        """Test locked getter/setter."""
        old_value = domain.locked
        new_value = not old_value
        bad_value = "foo"
        # set new_value
        try:
            domain.locked = new_value
            assert domain.locked == new_value
        except DomainUnlockTimeError:
            assert domain.locked == old_value
            new_value = old_value
        # set bad_value
        with pytest.raises(TypeError):
            domain.locked = bad_value
        assert domain.locked == new_value
        # re-set to old value
        domain.locked = old_value
        assert domain.locked == old_value
