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
"""Test classes for namedotcom console script."""


from __future__ import print_function
from __future__ import unicode_literals

import os

from click.testing import CliRunner

from pynamedotcom.cli import main


class TestCLI(object):
    """Test cases."""

    @staticmethod
    def invoke(args=None):
        """Invoke the command with the supplied arguments."""
        host = "api.dev.name.com"
        path = os.path.join(os.path.dirname(__file__), "auth.json")
        args = ["--auth-file", path, "--host", host] + args
        runner = CliRunner()
        return runner.invoke(main, args)

    def test_ping(self):
        """Test ping command."""
        args = ["ping"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert "OK" in result.output
