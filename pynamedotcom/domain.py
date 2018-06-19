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
"""pynamedotcom Domain module."""

from __future__ import print_function
from __future__ import unicode_literals

import logging

from requests.exceptions import HTTPError

from pynamedotcom.contact import Contact
from pynamedotcom.decorators import readonly, refresh, require_type
from pynamedotcom.exceptions import DomainUnlockTimeError


class Domain(object):
    """Domain class."""

    def __init__(self, session, **kwargs):
        """Construct Domain object instance."""
        self.session = session
        self._set(**kwargs)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.name)

    def _set(self, domainName, nameservers=None, contacts=None,
             privacyEnabled=None, locked=None, autorenewEnabled=None,
             expireDate=None, createDate=None, renewalPrice=None):
        """Set local properties."""
        self._name = domainName
        self._nameservers = nameservers
        self._privacy = privacyEnabled
        self._locked = locked
        self._autorenew = autorenewEnabled
        self._expiry = expireDate
        self._created = createDate
        self._renewal_price = renewalPrice
        if contacts is not None:
            self._contacts = {}
            for role, contact in contacts.items():
                self._contacts[role] = Contact(session=self.session, **contact)

    def _refresh(self):
        """Retrieve domain properties."""
        resp = self.session._get(endpoint="domains/{}".format(self.name))
        self._set(**resp.json())

    @property
    @refresh
    def name(self):
        return self._name

    @name.setter
    @readonly
    def name(self, value):
        pass

    @property
    @refresh
    def nameservers(self):
        return self._nameservers

    @nameservers.setter
    def nameservers(self, value):
        raise NotImplementedError

    @property
    @refresh
    def contacts(self):
        return self._contacts

    @contacts.setter
    def contacts(self, value):
        raise NotImplementedError

    @property
    @refresh
    def privacy(self):
        return self._privacy

    @privacy.setter
    def privacy(self, value):
        raise NotImplementedError

    @property
    @refresh
    def locked(self):
        return self._locked

    @locked.setter
    @require_type(bool)
    def locked(self, value):
        logging.getLogger(__name__).debug(
            "setting {}.locked = {}".format(self, value))
        if value:
            endpoint = "domains/{}:lock".format(self.name)
        else:
            endpoint = "domains/{}:unlock".format(self.name)
        try:
            resp = self.session._post(endpoint=endpoint)
            self._set(**resp.json())
        except HTTPError as e:
            resp = e.response
            data = resp.json()
            if resp.status_code == 400 \
                    and "Domain can not be unlocked until" in data["details"]:
                raise DomainUnlockTimeError(data["details"])
            else:
                raise e
        return self

    @property
    @refresh
    def autorenew(self):
        return self._autorenew

    @autorenew.setter
    def autorenew(self, value):
        raise NotImplementedError

    @property
    @refresh
    def expiry(self):
        return self._expiry

    @expiry.setter
    @readonly
    def expiry(self, value):
        pass

    @property
    @refresh
    def created(self):
        return self._created

    @created.setter
    @readonly
    def created(self, value):
        pass

    @property
    @refresh
    def renewal_price(self):
        return self._renewal_price

    @renewal_price.setter
    @readonly
    def renewal_price(self, value):
        pass
