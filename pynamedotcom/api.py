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
"""pynamedotcom Package."""

from __future__ import print_function
from __future__ import unicode_literals

import requests
from requests.auth import HTTPBasicAuth


class API(object):
    """API client library class."""

    def __init__(self, user=None, token=None,
                 host="api.name.com", version=4):
        """Construct API instance."""
        self.base_url = "https://{}/v{}".format(host, version)
        self.auth = HTTPBasicAuth(user, token)

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit context manager."""
        pass

    def ping(self):
        """Check service reachability."""
        url = "{}/hello".format(self.base_url)
        requests.get(url, auth=self.auth)
