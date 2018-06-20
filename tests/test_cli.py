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
import re

from click.testing import CliRunner

from pynamedotcom.contact import ROLES
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
            assert keyword in result.output

    def test_get_domain_name(self):
        """Test domain name retrieval."""
        name = "maddison.family"
        args = ["domain", name, "name"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert name in result.output

    def test_get_set_domain_nameservers(self):
        """Test getting/setting domain nameservers."""
        name = "maddison.family"
        args = ["domain", name, "nameservers"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        old_value = result.output.splitlines()
        new_value = ["ns1.example.com", "ns2.example.com"]
        result = self.invoke(args=args + new_value)
        assert result.exit_code == 0
        assert result.output == "OK\n"
        result = self.invoke(args=args + old_value)
        assert result.exit_code == 0
        assert result.output == "OK\n"
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert result.output.splitlines() == old_value

    def test_get_domain_contacts(self):
        """Test domain contacts retrieval."""
        name = "maddison.family"
        args = ["domain", name, "contacts"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        for role in ROLES:
            assert role in result.output

    def test_get_domain_privacy(self):
        """Test domain privacy state retrieval."""
        name = "maddison.family"
        args = ["domain", name, "privacy"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert result.output in ["True\n", "False\n"]

    def test_get_set_domain_locked(self):
        """Test getting/setting domain lock state."""
        name = "maddison.family"
        args = ["domain", name, "locked"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert result.output.rstrip() in ["True", "False"]
        old_value = result.output.splitlines()
        if result.output == "True\n":
            new_value = ["no"]
        else:
            new_value = ["yes"]
        result = self.invoke(args=args + new_value)
        assert (result.exit_code == 0 and result.output == "OK\n") or \
               (result.exit_code == 2 and "Domain can not be unlocked until" in result.output)  # noqa
        result = self.invoke(args=args + old_value)
        assert result.exit_code == 0
        assert result.output == "OK\n"
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert result.output.splitlines() == old_value

    def test_get_set_domain_autorenew(self):
        """Test getting/setting domain autorenew state."""
        name = "maddison.family"
        args = ["domain", name, "autorenew"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert result.output.rstrip() in ["True", "False"]
        old_value = result.output.splitlines()
        if result.output == "True\n":
            new_value = ["no"]
        else:
            new_value = ["yes"]
        result = self.invoke(args=args + new_value)
        assert result.exit_code == 0
        assert result.output == "OK\n"
        result = self.invoke(args=args + old_value)
        assert result.exit_code == 0
        assert result.output == "OK\n"
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert result.output.splitlines() == old_value

    def test_get_domain_expiry(self):
        """Test domain expiry date retrieval."""
        name = "maddison.family"
        args = ["domain", name, "expiry"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', result.output)

    def test_get_domain_created(self):
        """Test domain creation date retrieval."""
        name = "maddison.family"
        args = ["domain", name, "created"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', result.output)

    def test_get_domain_renewal_price(self):
        """Test domain renewal price retrieval."""
        name = "maddison.family"
        args = ["domain", name, "renewal_price"]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert re.match(r'\$\d+.\d{2}', result.output)

    def test_search_available(self):
        """Test successful availablility search."""
        name = "maddison.name"
        args = ["search", name]
        result = self.invoke(args=args)
        assert result.exit_code == 0
        assert name in result.output
        for keyword in ["premium", "type", "purchase price", "renewal price"]:
            assert keyword in result.output

    def test_search_unavailable(self):
        """Test unsuccessful availablility search."""
        name = "maddison.family"
        args = ["search", name]
        result = self.invoke(args=args)
        assert result.exit_code == 1
        assert name in result.output
        for keyword in ["premium", "type", "purchase price", "renewal price"]:
            assert keyword not in result.output
