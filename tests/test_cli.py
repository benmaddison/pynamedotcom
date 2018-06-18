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

import json
import os

from click.testing import CliRunner

from pynamedotcom.cli import main


class TestCLI(object):
    """Test cases."""

    @staticmethod
    def invoke(args=None, debug=False, auth_file=True,
               host="api.dev.name.com"):
        """Invoke the command with the supplied arguments."""
        base_args = ["--host", host]
        path = os.path.join(os.path.dirname(__file__), "auth.json")
        if auth_file:
            base_args += ["--auth-file", path]
        else:
            with open(path) as f:
                auth = json.load(f)
            base_args += ["--username", auth["user"],
                          "--token", auth["token"]]
        if debug:
            base_args.append("--debug")
        args = base_args + args
        runner = CliRunner()
        return runner.invoke(main, args)

    def test_ping(self):
        """Test ping command."""
        args = ["ping"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert "OK" in result.output

    def test_ping_debug(self):
        """Test ping command with debugging enabled."""
        args = ["ping"]
        result = self.invoke(args=args, debug=True)
        assert result.exit_code == 0
        assert "OK" in result.output

    def test_ping_credentials(self):
        """Test ping command with explicit credentials."""
        args = ["ping"]
        result = self.invoke(args=args, auth_file=False)
        assert result.exit_code == 0
        assert "OK" in result.output

    def test_get_domains(self):
        """Test domain list retrieval."""
        args = ["domains"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert "maddison.family" in result.output

    def test_get_domain(self):
        """Test domain detail retrieval."""
        name = "maddison.family"
        args = ["domain", name]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert name in result.output
        for keyword in ["nameservers", "contacts", "privacy", "locked",
                        "autorenew", "expiry", "created", "renewal price"]:
            keyword in result.output
