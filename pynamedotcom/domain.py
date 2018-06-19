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
from pynamedotcom.decorators import require_type
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

    def __getattr__(self, name):
        """Get private attributes."""
        try:
            if self.__getattribute__("_{}".format(name)) is None:
                self._refresh()
            return self.__getattribute__("_{}".format(name))
        except AttributeError:
            raise AttributeError("{} object has no attribute {}"
                                 .format(self.__class__, name))

    @property
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
