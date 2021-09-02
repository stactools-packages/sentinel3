import logging

import pystac
from pystac.extensions.eo import EOExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.sat import SatExtension

from .constants import SENTINEL_CONSTELLATION, SENTINEL_PROVIDER
from .metadata_links import MetadataLinks
from .product_metadata import ProductMetadata
from .properties import (fill_eo_properties, fill_proj_properties,
                         fill_sat_properties)

logger = logging.getLogger(__name__)


def create_item(granule_href: str) -> pystac.Item:
    """Create a STC Item from a Sentinel-3 scene.

    Args:
        granule_href (str): The HREF to the granule.
            This is expected to be a path to a SEN3 archive.

    Returns:
        pystac.Item: An item representing the Sentinel-3 OLCI or SLSTR scene.
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

    # ---- Add Extensions ----
    # sat
    sat = SatExtension.ext(item, add_if_missing=True)
    fill_sat_properties(sat, metalinks.product_metadata_href)

    # eo
    eo = EOExtension.ext(item, add_if_missing=True)
    fill_eo_properties(eo, metalinks.product_metadata_href)

    # proj
    proj = ProjectionExtension.ext(item, add_if_missing=True)
    fill_proj_properties(proj, product_metadata)

    # s3 properties
    item.properties.update({**product_metadata.metadata_dict})

    # --Common metadata--
    item.common_metadata.providers = [SENTINEL_PROVIDER]
    item.common_metadata.platform = product_metadata.platform
    item.common_metadata.constellation = SENTINEL_CONSTELLATION

    # Add assets to item
    item.add_asset(*metalinks.create_manifest_asset())

    # objects for bands
    item.add_asset(*metalinks.create_band_asset())

    return item
