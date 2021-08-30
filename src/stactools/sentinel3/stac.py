import logging
import os

import pystac
from pystac.extensions.eo import EOExtension
from pystac.extensions.sat import SatExtension
from pystac.extensions.projection import ProjectionExtension

from .metadata_links import MetadataLinks
from .product_metadata import ProductMetadata

from .constants import (
    SENTINEL_PROVIDER,
    SENTINEL_CONSTELLATION,
    SENTINEL_LICENSE,
)

from .properties import (
    fill_sat_properties,
    fill_proj_properties,
    fill_eo_properties
)

from .bands import image_asset_from_href

logger = logging.getLogger(__name__)


def create_item(granule_href: str) -> pystac.Item:
    """Create a STC Item from a Sentinel-3 scene.

    Args:
        granule_href (str): The HREF to the granule.
            This is expected to be a path to a SAFE archive.

    Returns:
        pystac.Item: An item representing the Sentinel-1 GRD scene.
    """

    metalinks = MetadataLinks(granule_href)

    product_metadata = ProductMetadata(metalinks.product_metadata_href)

    item = pystac.Item(
        id=product_metadata.scene_id,
        geometry=product_metadata.geometry,
        bbox=product_metadata.bbox,
        datetime=product_metadata.get_datetime,
        properties={},
        stac_extensions=[],
    )
    
    return item