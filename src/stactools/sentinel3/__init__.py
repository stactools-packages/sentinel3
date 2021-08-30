import stactools.core

from stactools.sentinel3.stac import create_item

__all__ = ['create_collection', 'create_item']

stactools.core.use_fsspec()


def register_plugin(registry):
    from stactools.sentinel3 import commands
    registry.register_subcommand(commands.create_sentinel3_command)


__version__ = "0.1.0"
