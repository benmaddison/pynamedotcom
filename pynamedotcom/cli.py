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
"""pynamedotcom API module."""

from __future__ import print_function

import click
import json
import logging

from pynamedotcom import API


logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
@click.option("-d", "--debug", is_flag=True,
              help="Enable debug logging.")
@click.option("-h", "--host", default="api.name.com",
              help="Server hostname.", show_default=True)
@click.option("-u", "--username",
              help="name.com username.")
@click.option('-t', "--token",
              help="name.com API token.")
@click.option("-f", "--auth-file", type=click.Path(exists=True),
              help="Read credentials from file.")
def main(ctx, host, debug, auth_file, username, token):
    """CLI tool for interacting with the name.com API."""
    # Configure logging
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING
    logging.basicConfig(level=log_level)
    # Get credentials from file or CLI options
    if auth_file:
        with open(auth_file) as f:
            auth = json.load(f)
    else:
        auth = {"user": username, "token": token}
    logger.debug("connecting to {} as {}".format(host, auth["user"]))

    def api():
        """Helper function to return configured pynamedotcom.API instance."""
        return API(host=host, **auth)
    # Add helper to click Context.obj to pass to command functions
    ctx.obj = api


@main.command()
@click.pass_context
def ping(ctx):
    """Check for successful authentication."""
    # Use provided helper to instantiate pynamedotcom.API object
    with ctx.obj() as api:
        try:
            # Execute method and print a success message
            api.ping()
            click.echo(click.style("OK", fg="green"))
        except Exception as e:
            # Raise the correct exception on failure
            raise click.ClickException(click.style("{}".format(e), fg="red"))


if __name__ == "__main__":
    main()
