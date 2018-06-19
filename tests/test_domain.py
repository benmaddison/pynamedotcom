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
"""Test classes for pynamedotcom domain module."""


from __future__ import print_function
from __future__ import unicode_literals

import pytest
import re

from pynamedotcom.contact import Contact
from pynamedotcom.exceptions import (DomainUnlockTimeError,
                                     NameserverUpdateError)


class TestDomain(object):
    """Domain test cases."""

    def test_refresh(self, domain):
        """Test refresh method."""
        assert domain.name == domain.refresh().name

    def test_name_property(self, domain):
        """Test name property."""
        old_value = "maddison.family"
        new_value = "example.com"
        assert domain.name == old_value
        with pytest.raises(AttributeError, match=r'read-only'):
            domain.name = new_value

    def test_nameservers_property(self, domain):
        """Test nameservers property."""
        old_value = domain.nameservers
        new_value = ["ns1.example.com", "ns2.example.com"]
        new_value_missing_glue = ["ns.{}".format(domain.name)]
        bad_value = "foo"
        # set new_value
        domain.nameservers = new_value
        assert domain.nameservers == new_value
        # set new_value_missing_glue
        with pytest.raises(NameserverUpdateError):
            domain.nameservers = new_value_missing_glue
        assert domain.nameservers == new_value
        # set bad_value
        with pytest.raises(TypeError):
            domain.nameservers = bad_value
        assert domain.nameservers == new_value
        # re-set to old value
        domain.nameservers = old_value
        assert domain.nameservers == old_value

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_contacts_property(self, domain):
        """Test contacts property."""
        old_value = domain.contacts
        new_value = {
            "admin": Contact(session=domain.session),
            "tech": Contact(session=domain.session),
            "registrant": Contact(session=domain.session),
            "billing": Contact(session=domain.session)
        }
        bad_value = "foo"
        # set new_value
        domain.contacts = new_value
        assert domain.contacts == new_value
        # set bad_value
        with pytest.raises(TypeError):
            domain.contacts = bad_value
        assert domain.contacts == new_value
        # re-set to old value
        domain.contacts = old_value
        assert domain.contacts == old_value

    @pytest.mark.xfail(raises=NotImplementedError)
    def test_privacy_property(self, domain):
        """Test privacy property."""
        old_value = domain.privacy
        new_value = not old_value
        bad_value = "foo"
        # set new_value
        domain.privacy = new_value
        assert domain.privacy == new_value
        # set bad_value
        with pytest.raises(TypeError):
            domain.privacy = bad_value
        assert domain.privacy == new_value
        # re-set to old value
        domain.privacy = old_value
        assert domain.privacy == old_value

    def test_locked_property(self, domain):
        """Test locked property."""
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

    def test_autorenew_property(self, domain):
        """Test autorenew property."""
        old_value = domain.autorenew
        new_value = not old_value
        bad_value = "foo"
        # set new_value
        domain.autorenew = new_value
        assert domain.autorenew == new_value
        # set bad_value
        with pytest.raises(TypeError):
            domain.autorenew = bad_value
        assert domain.autorenew == new_value
        # re-set to old value
        domain.autorenew = old_value
        assert domain.autorenew == old_value

    def test_expiry_property(self, domain):
        """Test expiry property."""
        assert re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',
                        domain.expiry)
        new_value = "2025-06-15T10:25:05Z"
        with pytest.raises(AttributeError, match=r'read-only'):
            domain.expiry = new_value

    def test_created_property(self, domain):
        """Test created property."""
        assert re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z',
                        domain.created)
        new_value = "2025-06-15T10:25:05Z"
        with pytest.raises(AttributeError, match=r'read-only'):
            domain.created = new_value

    def test_renewal_price_property(self, domain):
        """Test renewal_price property."""
        old_value = domain.renewal_price
        assert isinstance(old_value, float)
        new_value = old_value + 10
        with pytest.raises(AttributeError, match=r'read-only'):
            domain.renewal_price = new_value
