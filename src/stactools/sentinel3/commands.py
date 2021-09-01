import logging
import os

import click

from stactools.sentinel3.stac import create_item

logger = logging.getLogger(__name__)


def create_sentinel3_command(cli):
    """Creates the stactools-sentinel3 command line utility."""
    @cli.group(
        "sentinel3",
        short_help=("Commands for working with stactools-sentinel3"),
    )
    def sentinel3():
        pass

    @sentinel3.command(
        "create-item",
        short_help="Convert a Sentinel3 scene into a STAC item",
    )
    @click.argument("src")
    @click.argument("dst")
    def create_item_command(src, dst):
        """Creates a STAC Collection

        Args:
            src (str): path to the scene
            dst (str): path to the STAC Item JSON file that will be created
        """
        item = create_item(src)

        item_path = os.path.join(dst, "{}.json".format(item.id))
        item.set_self_href(item_path)

        item.save_object()

        return sentinel3
