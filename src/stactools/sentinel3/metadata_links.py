import os
from typing import List, Optional

import pystac
from stactools.core.io import ReadHrefModifier
from stactools.core.io.xml import XmlElement

from .constants import (SAFE_MANIFEST_ASSET_KEY, SENTINEL_OLCI_BANDS,
                        SENTINEL_SLSTR_BANDS, SENTINEL_SRAL_BANDS,
                        SENTINEL_SYNERGY_BANDS, MANIFEST_FILENAME)


class ManifestError(Exception):
    pass


class MetadataLinks:
    def __init__(self,
                 granule_href: str,
                 read_href_modifier: Optional[ReadHrefModifier] = None):
        self.granule_href = granule_href
        self.href = os.path.join(granule_href, MANIFEST_FILENAME)

        self.manifest = XmlElement.from_file(self.href, read_href_modifier)
        data_object_section = self.manifest.find("dataObjectSection")
        if data_object_section is None:
            raise ManifestError(
                f"Manifest at {self.href} does not have a dataObjectSection")

        self._data_object_section = data_object_section
        self.product_metadata_href = os.path.join(granule_href,
                                                  MANIFEST_FILENAME)

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

    def create_band_asset(self, manifest: XmlElement):

        band_dict_list = []

        product_type = manifest.findall(".//sentinel3:productType")[0].text
        product_type_category = product_type.split("_")[0]

        if product_type_category == "OL":
            instrument_bands = SENTINEL_OLCI_BANDS
        elif product_type_category == "SL":
            instrument_bands = SENTINEL_SLSTR_BANDS
        elif product_type_category == "SR":
            instrument_bands = SENTINEL_SRAL_BANDS
        elif product_type_category == "SY":
            instrument_bands = SENTINEL_SYNERGY_BANDS
        else:
            raise RuntimeError(
                f"Unknown product type encountered: {product_type_category}")

        if instrument_bands == SENTINEL_SRAL_BANDS:
            for band in instrument_bands:
                band_dict = {
                    "name": instrument_bands[band].name,
                    "description": instrument_bands[band].description,
                    "central_frequency":
                    instrument_bands[band].center_wavelength,
                    "band_width_in_Hz":
                    instrument_bands[band].full_width_half_max
                }
                band_dict_list.append(band_dict)
        elif instrument_bands == SENTINEL_SYNERGY_BANDS:
            if "AOD" in product_type:
                key_list = list(SENTINEL_SYNERGY_BANDS.keys())[26:32]
            elif "SYN" in product_type:
                key_list = list(SENTINEL_SYNERGY_BANDS.keys())[:26]
            else:
                key_list = list(SENTINEL_SYNERGY_BANDS.keys())[-4:]
            for band in key_list:
                band_dict = {
                    "name": instrument_bands[band].name,
                    "description": instrument_bands[band].description,
                    "center_wavelength":
                    instrument_bands[band].center_wavelength,
                    "band_width": instrument_bands[band].full_width_half_max
                }
                band_dict_list.append(band_dict)
        else:
            for band in instrument_bands:
                band_dict = {
                    "name": instrument_bands[band].name,
                    "description": instrument_bands[band].description,
                    "center_wavelength":
                    instrument_bands[band].center_wavelength,
                    "band_width": instrument_bands[band].full_width_half_max
                }
                band_dict_list.append(band_dict)

        asset = pystac.Asset(href=self.href,
                             media_type=pystac.MediaType.XML,
                             roles=["metadata"],
                             extra_fields={"band_fields": band_dict_list})
        return ("eo:bands", asset)
