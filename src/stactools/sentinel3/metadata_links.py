import os
from typing import List, Optional

import pystac
from stactools.core.io.xml import XmlElement

from .constants import (SAFE_MANIFEST_ASSET_KEY, SENTINEL_OLCI_BANDS,
                        SENTINEL_SLSTR_BANDS)


class ManifestError(Exception):
    pass


class MetadataLinks:
    def __init__(
        self,
        granule_href: str,
    ):
        self.granule_href = granule_href
        self.href = os.path.join(granule_href, "xfdumanifest.xml")

        root = XmlElement.from_file(self.href)
        data_object_section = root.find("dataObjectSection")
        if data_object_section is None:
            raise ManifestError(
                f"Manifest at {self.href} does not have a dataObjectSection")

        self._data_object_section = data_object_section
        self.product_metadata_href = os.path.join(granule_href,
                                                  "xfdumanifest.xml")

    def _find_href(self, xpaths: List[str]) -> Optional[str]:
        file_path = None
        for xpath in xpaths:
            file_path = self._data_object_section.find_attr("href", xpath)
            if file_path is not None:
                break

        if file_path is None:
            return None
        else:
            # Remove relative prefix that some paths have
            file_path = file_path.strip("./")
            return os.path.join(self.granule_href, file_path)

    @property
    def thumbnail_href(self) -> Optional[str]:
        preview = os.path.join(self.granule_href, "preview")
        return os.path.join(preview, "quick-look.png")

    def create_manifest_asset(self):
        asset = pystac.Asset(
            href=self.href,
            media_type=pystac.MediaType.XML,
            roles=["metadata"],
        )
        return (SAFE_MANIFEST_ASSET_KEY, asset)

    def create_band_asset(self):

        band_dict_list = []

        root = XmlElement.from_file(self.product_metadata_href)
        product_type = root.findall(".//sentinel3:productType")[0].text.split(
            "_")[0]

        if product_type == "OL":
            instrument_bands = SENTINEL_OLCI_BANDS
        elif product_type == "SL":
            instrument_bands = SENTINEL_SLSTR_BANDS

        for band in instrument_bands:
            band_dict = {
                "name": instrument_bands[band].name,
                "description": instrument_bands[band].description,
                "center_wavelength": instrument_bands[band].center_wavelength,
                "band_width": instrument_bands[band].full_width_half_max
            }
            band_dict_list.append(band_dict)

        asset = pystac.Asset(href=self.href,
                             media_type=pystac.MediaType.XML,
                             roles=["metadata"],
                             extra_fields={"band_fields": band_dict_list})
        return ("eo:bands", asset)
