import logging
import os
from typing import Optional

import pystac
from pystac.extensions.eo import EOExtension
from pystac.extensions.sat import SatExtension
from stactools.core.io import ReadHrefModifier

from .constants import (MANIFEST_FILENAME, SENTINEL_CONSTELLATION,
                        SENTINEL_LICENSE, SENTINEL_PROVIDER)
from .file_extension_updated import FileExtensionUpdated
from .metadata_links import MetadataLinks
from .product_metadata import ProductMetadata
from .properties import (fill_eo_properties, fill_file_properties,
                         fill_manifest_file_properties, fill_sat_properties)

logger = logging.getLogger(__name__)


def create_item(
        granule_href: str,
        skip_nc: bool = False,
        read_href_modifier: Optional[ReadHrefModifier] = None) -> pystac.Item:
    """Create a STC Item from a Sentinel-3 scene.

    Args:
        granule_href (str): The HREF to the granule.
            This is expected to be a path to a SEN3 archive.
        skip_nc (bool): Skip parsing NetCDF data files. Since these are large, this saves
            bandwidth when working over network, at the cost of metadata we can obtain
            from them. Defaults to False.
        read_href_modifier: A function that takes an HREF and returns a modified HREF.
            This can be used to modify a HREF to make it readable, e.g. appending
            an Azure SAS token or creating a signed URL.

    Returns:
        pystac.Item: An item representing the Sentinel-3 OLCI or SLSTR scene.
    """

    metalinks = MetadataLinks(granule_href, read_href_modifier)

    product_metadata = ProductMetadata(granule_href, metalinks.manifest)

    item = pystac.Item(
        id=product_metadata.scene_id,
        geometry=product_metadata.geometry,
        bbox=product_metadata.bbox,
        datetime=product_metadata.get_datetime,
        properties={},
        stac_extensions=[
            "https://stac-extensions.github.io/file/v2.1.0/schema.json"
        ],
    )

    # ---- Add Extensions ----
    # sat
    sat = SatExtension.ext(item, add_if_missing=True)
    fill_sat_properties(sat, metalinks.manifest)

    # eo
    eo = EOExtension.ext(item, add_if_missing=True)
    fill_eo_properties(eo, metalinks.manifest)

    # s3 properties
    item.properties.update({**product_metadata.metadata_dict})

    # --Common metadata--
    item.common_metadata.providers = [SENTINEL_PROVIDER]
    item.common_metadata.platform = product_metadata.platform
    item.common_metadata.constellation = SENTINEL_CONSTELLATION

    # Add assets to item
    manifest_asset_key, manifest_asset = metalinks.create_manifest_asset()
    item.add_asset(manifest_asset_key, manifest_asset)
    manifest_href = os.path.join(granule_href, MANIFEST_FILENAME)
    manifest_file = FileExtensionUpdated.ext(manifest_asset,
                                             add_if_missing=True)
    fill_manifest_file_properties(manifest_href, metalinks.manifest_text,
                                  manifest_file)

    # create band asset list
    band_list, asset_identifier_list, asset_list = metalinks.create_band_asset(
        metalinks.manifest, skip_nc)

    band_list = [
        key.replace("_Data", "").replace("Data", "", 1) for key in band_list
    ]

    # objects for bands
    for band, identifier, asset in zip(band_list, asset_identifier_list,
                                       asset_list):
        item.add_asset(band, asset)
        file = FileExtensionUpdated.ext(asset, add_if_missing=True)
        fill_file_properties(metalinks.granule_href, identifier, file,
                             metalinks.manifest)

    # license link
    item.links.append(SENTINEL_LICENSE)

    return item
