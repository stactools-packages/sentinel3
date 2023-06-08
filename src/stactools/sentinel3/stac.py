import logging
import os
import re
from decimal import Decimal
from typing import Any, List, Optional

import pystac
from pystac.extensions.eo import EOExtension
from pystac.extensions.sat import SatExtension
from stactools.core.io import ReadHrefModifier

from .constants import (
    MANIFEST_FILENAME,
    SENTINEL_CONSTELLATION,
    SENTINEL_PROVIDER,
    SPECIAL_ASSET_KEYS,
)
from .file_extension_updated import FileExtensionUpdated
from .metadata_links import MetadataLinks
from .product_metadata import ProductMetadata
from .properties import (
    fill_eo_properties,
    fill_file_properties,
    fill_manifest_file_properties,
    fill_sat_properties,
)

logger = logging.getLogger(__name__)


# This module includes copious contributions ported from the Microsoft Planetary
# Computer Sentinel-3 dataset package:
# https://github.com/microsoft/planetary-computer-tasks/blob/main/datasets/sentinel-3/


def recursive_round(coordinates: List[Any], precision: int) -> List[Any]:
    """Rounds a list of numbers. The list can contain additional nested lists
    or tuples of numbers.

    Any tuples encountered will be converted to lists.

    Args:
        coordinates (List[Any]): A list of numbers, possibly containing nested
            lists or tuples of numbers.
        precision (int): Number of decimal places to use for rounding.

    Returns:
        List[Any]: The list of numbers rounded to the given precision.
    """
    rounded: List[Any] = []
    for value in coordinates:
        if isinstance(value, (int, float)):
            rounded.append(round(value, precision))
        else:
            rounded.append(recursive_round(list(value), precision))
    return rounded


def nano2micro(value: float) -> float:
    """Converts nanometers to micrometers while handling floating
    point arithmetic errors."""
    return float(Decimal(str(value)) / Decimal("1000"))


def hz2ghz(value: float) -> float:
    """Converts hertz to gigahertz while handling floating point
    arithmetic errors."""
    return float(Decimal(str(value)) / Decimal("1000000000"))


def sen3_to_kebab(asset_key: str) -> str:
    """Converts asset_key to a clean kebab case"""
    if asset_key in SPECIAL_ASSET_KEYS:
        return SPECIAL_ASSET_KEYS[asset_key]

    # purge Data suffix
    asset_key = asset_key.replace("_Data", "").replace("Data", "", 1)

    new_asset_key = ""
    for first, second in zip(asset_key, asset_key[1:]):
        new_asset_key += first.lower()
        if first.islower() and second.isupper():
            new_asset_key += "-"
    new_asset_key += asset_key[-1].lower()
    new_asset_key = new_asset_key.replace("_", "-")
    return new_asset_key


def sen3_to_snake(key: str) -> str:
    new_key = "".join("_" + char.lower() if char.isupper() else char for char in key)
    # strip "_pixels_percentages" to match eo:cloud_cover pattern
    if new_key.endswith("_pixels_percentage"):
        new_key = new_key.replace("_pixels_percentage", "")
    elif new_key.endswith("_pixelss_percentage"):
        new_key = new_key.replace("_pixelss_percentage", "")
    elif new_key.endswith("_percentage"):
        new_key = new_key.replace("_percentage", "")
    return new_key


def product_type(source, datatype):
    source_to_name = {"OL": "olci", "SL": "slstr", "SR": "sral", "SY": "synergy"}
    return f"{source_to_name[source]}-{datatype.strip('_').lower()}"


def create_item(
    granule_href: str,
    skip_nc: bool = False,
    read_href_modifier: Optional[ReadHrefModifier] = None,
) -> pystac.Item:
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
        stac_extensions=["https://stac-extensions.github.io/file/v2.1.0/schema.json"],
    )
    sen3naming = re.match(
        r".*/(?P<mission>...)_(?P<source>[A-Z]{2})_(?P<level>[_012])_(?P<datatype>.{6})"
        r"_(?P<datastart>.{15})_(?P<datastop>.{15})_(?P<creation>.{15})"
        r"_(?P<instance_id>((?P<duration>[0-9]{4})_(?P<cycle>[0-9]{3})"
        r"_(?P<relative_orbit>[0-9]{3})"
        r"_(?P<frame>[0-9]{4}))|.{17})_(?P<generating_centre>...)"
        r"_(?P<platform>[OFDR])_(?P<timeliness>[^_]+)_(?P<collection>[^\.]+)\.SEN3",
        granule_href,
    )
    if not sen3naming:
        raise ValueError(
            "Granule name does not match SEN3 naming convention(s)", granule_href
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

    if item.common_metadata.instruments == ["SYNERGY"]:
        # "SYNERGY" is not a instrument
        item.properties["instruments"] = ["OLCI", "SLSTR"]

    # --Extended Sentinel3 metadata--
    # Add the processing timelessness to the properties
    item.properties["s3:processing_timeliness"] = sen3naming["timeliness"]

    # Add a user-friendly name
    item.properties["s3:product_name"] = product_type(
        *sen3naming.group("source", "datatype")
    )
    # Providers should be supplied in the Collection, not the Item
    item.properties.pop("providers", None)

    # start_datetime and end_datetime are incorrectly formatted
    item.properties["start_datetime"] = pystac.utils.datetime_to_str(
        pystac.utils.str_to_datetime(sen3naming["datastart"])
    )
    item.properties["end_datetime"] = pystac.utils.datetime_to_str(
        pystac.utils.str_to_datetime(sen3naming["datastop"])
    )
    item.properties["datetime"] = pystac.utils.datetime_to_str(
        pystac.utils.str_to_datetime(sen3naming["creation"])
    )

    # Remove s3:mode, which is always set to EO (Earth # Observation). It
    # offers no additional information.
    item.properties.pop("s3:mode", None)

    new_props = {}
    for key, value in item.properties.items():
        if key.startswith("s3:"):
            new_props[sen3_to_snake(key)] = value
        else:
            new_props[key] = value
    item.properties = new_props

    # Add assets to item
    manifest_asset_key, manifest_asset = metalinks.create_manifest_asset()
    item.add_asset(manifest_asset_key, manifest_asset)
    manifest_href = os.path.join(granule_href, MANIFEST_FILENAME)
    manifest_file = FileExtensionUpdated.ext(manifest_asset, add_if_missing=True)
    fill_manifest_file_properties(manifest_href, metalinks.manifest_text, manifest_file)

    # create band asset list
    band_list, asset_identifier_list, asset_list = metalinks.create_band_asset(
        metalinks.manifest, skip_nc
    )

    band_list = [sen3_to_kebab(key) for key in band_list]

    # objects for bands
    for band, identifier, asset in zip(band_list, asset_identifier_list, asset_list):
        item.add_asset(band, asset)
        file = FileExtensionUpdated.ext(asset, add_if_missing=True)
        fill_file_properties(
            metalinks.granule_href, identifier, file, metalinks.manifest
        )

    # ---- ASSETS ----
    for asset_key, asset in item.assets.items():
        # remove local paths
        asset.extra_fields.pop("file:local_path", None)

        # Add a description to the safe_manifest asset
        if asset_key == "safe-manifest":
            asset.description = "SAFE product manifest"

        # correct eo:bands
        if "eo:bands" in asset.extra_fields:
            for band in asset.extra_fields["eo:bands"]:
                band["center_wavelength"] = nano2micro(band["center_wavelength"])
                band["full_width_half_max"] = nano2micro(band["band_width"])
                band.pop("band_width")

        # Tune up the radar altimetry bands. Radar altimetry is different
        # enough than radar imagery that the existing SAR extension doesn't
        # quite work (plus, the SAR extension doesn't have a band object).
        # We'll use a band construct similar to eo:bands, but follow the
        # naming and unit conventions in the SAR extension.
        if "sral:bands" in asset.extra_fields:
            asset.extra_fields["s3:altimetry_bands"] = asset.extra_fields.pop(
                "sral:bands"
            )
            for band in asset.extra_fields["s3:altimetry_bands"]:
                band["frequency_band"] = band.pop("name")
                band["center_frequency"] = hz2ghz(band.pop("central_frequency"))
                band["band_width"] = hz2ghz(band.pop("band_width_in_Hz"))

    return item
