import os
from typing import List, Optional, Tuple

import netCDF4 as nc  # type: ignore
import pystac
from lxml import etree  # type: ignore
from stactools.core.io import ReadHrefModifier, read_text
from stactools.core.io.xml import XmlElement

from . import constants, xml


class ManifestError(Exception):
    pass


class MetadataLinks:
    def __init__(
        self, granule_href: str, read_href_modifier: Optional[ReadHrefModifier] = None
    ):
        self.granule_href = granule_href
        self.href = os.path.join(granule_href, constants.MANIFEST_FILENAME)

        self.manifest, self.manifest_text = self.parse_xml_from_href(
            self.href, read_href_modifier
        )
        data_object_section = self.manifest.find("dataObjectSection")
        if data_object_section is None:
            raise ManifestError(
                f"Manifest at {self.href} does not have a dataObjectSection"
            )

        self._data_object_section = data_object_section
        self.product_metadata_href = os.path.join(
            granule_href, constants.MANIFEST_FILENAME
        )

    @classmethod
    def parse_xml_from_href(
        cls, href: str, read_href_modifier: Optional[ReadHrefModifier] = None
    ) -> Tuple["XmlElement", str]:
        text = read_text(href, read_href_modifier)
        return XmlElement(etree.fromstring(bytes(text, encoding="utf-8"))), text

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

    def read_href(self, xpath: str) -> str:
        asset_location = self.manifest.find_attr("href", xpath)
        if asset_location is None:
            raise RuntimeError(f"Xpath returns no href: {xpath}")
        return asset_location

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
        return constants.SAFE_MANIFEST_ASSET_KEY, asset

    def _get_resolution(self, asset_href: str, skip_nc: bool) -> List[int]:
        if skip_nc:
            return []
        ds = nc.Dataset(asset_href)
        if hasattr(ds, "resolution"):
            asset_resolution_str = ds.resolution.strip("[] ")
            asset_resolution = [
                int(r) for r in reversed(asset_resolution_str.split(" "))
            ]
        elif hasattr(ds, "spatial_resolution"):
            spatres_str = ds.spatial_resolution
            tail = "km at nadir"
            if spatres_str.endswith(tail):
                asset_resolution_str = spatres_str.replace(tail, "")
                asset_resolution = [
                    int(asset_resolution_str) * 1000,
                    int(asset_resolution_str) * 1000,
                ]
            else:
                raise ValueError(
                    "Did not recognize 'spatial_resolution' string from " + asset_href
                )
        else:
            raise ValueError("Don't know how to pull resolution from " + asset_href)
        ds.close()
        return asset_resolution

    def create_band_asset(self, manifest: XmlElement, skip_nc=False):
        def strip_prefix(prefix: str, content: str) -> str:
            if content.startswith(prefix):
                return content[len(prefix) :]
            return content

        asset_identifier_list = []
        asset_list = []

        product_type = xml.find_text(manifest, ".//sentinel3:productType")
        product_type_category = product_type.split("_")[0]

        if product_type_category == "OL":
            instrument_bands = constants.SENTINEL_OLCI_BANDS
        elif product_type_category == "SL":
            instrument_bands = constants.SENTINEL_SLSTR_BANDS
        elif product_type_category == "SR":
            instrument_bands = constants.SENTINEL_SRAL_BANDS
        elif product_type_category == "SY":
            instrument_bands = constants.SENTINEL_SYNERGY_BANDS
        else:
            raise RuntimeError(
                f"Unknown product type encountered: {product_type_category}"
            )

        asset_key_list = None
        if instrument_bands == constants.SENTINEL_SRAL_BANDS:
            asset_key_list = constants.SRAL_L2_LAN_WAT_KEYS
            for asset_key in asset_key_list:
                band_dict_list = []
                for band in instrument_bands:
                    band_dict = {
                        "name": instrument_bands[band].name,
                        "description": instrument_bands[band].description,
                        "central_frequency": instrument_bands[band].center_wavelength,
                        "band_width_in_Hz": instrument_bands[band].full_width_half_max,
                    }
                    band_dict_list.append(band_dict)
                if "reduced" in asset_key:
                    band_dict_list = [band_dict_list[1]]
                else:
                    pass
                asset_location = self.read_href(
                    f".//dataObject[@ID='{asset_key}']//fileLocation"
                )
                asset_href = os.path.join(self.granule_href, asset_location)
                media_type = manifest.find_attr(
                    "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                )
                asset_description = manifest.find_attr(
                    "textInfo", f".//dataObject[@ID='{asset_key}']//fileLocation"
                )
                if skip_nc:
                    asset_shape_list: List[dict] = []
                else:
                    asset_shape_list = []
                    ds = nc.Dataset(asset_href)
                    for key in ds.dimensions.keys():
                        asset_shape_dict = {key: int(ds.dimensions[key].size)}
                        asset_shape_list.append(asset_shape_dict)
                    ds.close()
                asset_obj = pystac.Asset(
                    href=asset_href,
                    media_type=media_type,
                    description=asset_description,
                    roles=["data"],
                    extra_fields={
                        "shape": asset_shape_list,
                        "sral:bands": band_dict_list,
                    },
                )
                asset_identifier_list.append(asset_key)
                asset_list.append(asset_obj)
        elif instrument_bands == constants.SENTINEL_SYNERGY_BANDS:
            if "_AOD_" in product_type:
                band_key_list = list(constants.SENTINEL_SYNERGY_BANDS.keys())[26:32]
                asset_key_list = ["NTC_AOD_Data"]
                band_dict_list = []
                for asset_key in asset_key_list:
                    for band in band_key_list:
                        band_dict = {
                            "name": instrument_bands[band].name,
                            "description": instrument_bands[band].description,
                            "center_wavelength": instrument_bands[
                                band
                            ].center_wavelength,
                            "band_width": instrument_bands[band].full_width_half_max,
                        }
                        band_dict_list.append(band_dict)
                    asset_location = self.read_href(
                        f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_href = os.path.join(self.granule_href, asset_location)
                    media_type = manifest.find_attr(
                        "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                    )
                    asset_description = "Global aerosol parameters"
                    asset_resolution = self._get_resolution(asset_href, skip_nc)
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={
                            "s3:spatial_resolution": asset_resolution,
                            "eo:bands": band_dict_list,
                        },
                    )
                    asset_identifier_list.append(asset_key)
                    asset_list.append(asset_obj)
            elif "_SYN_" in product_type:
                asset_key_list = constants.SYNERGY_SYN_ASSET_KEYS
                for ind, asset_key in enumerate(asset_key_list):
                    if ind < 26:
                        band_key = list(constants.SENTINEL_SYNERGY_BANDS.keys())[ind]
                        band_dict_list = []
                        band_dict = {
                            "name": instrument_bands[band_key].name,
                            "description": instrument_bands[band_key].description,
                            "center_wavelength": instrument_bands[
                                band_key
                            ].center_wavelength,
                            "band_width": instrument_bands[
                                band_key
                            ].full_width_half_max,
                        }
                        band_dict_list.append(band_dict)
                    elif ind == 26 or ind == 27:
                        band_key_list = constants.SYNERGY_L2_A550_T550_BANDS
                        band_dict_list = []
                        for band in band_key_list:
                            band_dict = {
                                "name": constants.SENTINEL_OLCI_SLSTR_BANDS[band].name,
                                "description": constants.SENTINEL_OLCI_SLSTR_BANDS[
                                    band
                                ].description,
                                "center_wavelength": constants.SENTINEL_OLCI_SLSTR_BANDS[
                                    band
                                ].center_wavelength,
                                "band_width": constants.SENTINEL_OLCI_SLSTR_BANDS[
                                    band
                                ].full_width_half_max,
                            }
                            band_dict_list.append(band_dict)
                    elif ind == 28:
                        band_key_list = constants.SYNERGY_L2_SDR_BANDS
                        band_dict_list = []
                        for band in band_key_list:
                            band_dict = {
                                "name": constants.SENTINEL_OLCI_SLSTR_BANDS[band].name,
                                "description": constants.SENTINEL_OLCI_SLSTR_BANDS[
                                    band
                                ].description,
                                "center_wavelength": constants.SENTINEL_OLCI_SLSTR_BANDS[
                                    band
                                ].center_wavelength,
                                "band_width": constants.SENTINEL_OLCI_SLSTR_BANDS[
                                    band
                                ].full_width_half_max,
                            }
                            band_dict_list.append(band_dict)
                    else:
                        band_dict_list = []
                    asset_location = self.read_href(
                        f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_href = os.path.join(
                        self.granule_href, strip_prefix("./", asset_location)
                    )
                    media_type = manifest.find_attr(
                        "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                    )
                    asset_description = manifest.find_attr(
                        "textInfo", f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_resolution = self._get_resolution(asset_href, skip_nc)
                    if skip_nc:
                        asset_shape_list = []
                    else:
                        asset_shape_list = []
                        ds = nc.Dataset(asset_href)
                        for key in ds.dimensions.keys():
                            asset_shape_dict = {key: int(ds.dimensions[key].size)}
                            asset_shape_list.append(asset_shape_dict)
                        ds.close()
                    if band_dict_list:
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={
                                "s3:shape": asset_shape_list,
                                "s3:spatial_resolution": asset_resolution,
                                "eo:bands": band_dict_list,
                            },
                        )
                    else:
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={
                                "s3:shape": asset_shape_list,
                                "s3:spatial_resolution": asset_resolution,
                            },
                        )
                    asset_identifier_list.append(asset_key)
                    asset_list.append(asset_obj)
            elif any(product_id in product_type for product_id in ["_VG1_", "_V10_"]):
                asset_key_list = constants.SYNERGY_V10_VG1_ASSET_KEYS
                for ind, asset_key in enumerate(asset_key_list):
                    band_dict_list = []
                    if ind < 4:
                        band_key = list(constants.SENTINEL_SYNERGY_BANDS.keys())[-4:][
                            ind
                        ]
                        band_dict = {
                            "name": instrument_bands[band_key].name,
                            "description": instrument_bands[band_key].description,
                            "center_wavelength": instrument_bands[
                                band_key
                            ].center_wavelength,
                            "band_width": instrument_bands[
                                band_key
                            ].full_width_half_max,
                        }
                        band_dict_list.append(band_dict)
                    elif ind == 4:
                        band_key_list = ["B2", "B3"]
                        for band in band_key_list:
                            band_dict = {
                                "name": instrument_bands[band].name,
                                "description": instrument_bands[band].description,
                                "center_wavelength": instrument_bands[
                                    band
                                ].center_wavelength,
                                "band_width": instrument_bands[
                                    band
                                ].full_width_half_max,
                            }
                            band_dict_list.append(band_dict)
                    else:
                        band_dict_list = []
                    asset_location = self.read_href(
                        f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_href = os.path.join(
                        self.granule_href, strip_prefix("./", asset_location)
                    )
                    media_type = manifest.find_attr(
                        "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                    )
                    asset_description = manifest.find_attr(
                        "textInfo", f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_resolution = self._get_resolution(asset_href, skip_nc)
                    if skip_nc:
                        asset_shape_list = []
                    else:
                        asset_shape_list = []
                        ds = nc.Dataset(asset_href)
                        for key in ds.dimensions.keys():
                            asset_shape_dict = {key: int(ds.dimensions[key].size)}
                            asset_shape_list.append(asset_shape_dict)
                        ds.close()
                    if band_dict_list:
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={
                                "s3:shape": asset_shape_list,
                                "s3:spatial_resolution": asset_resolution,
                                "eo:bands": band_dict_list,
                            },
                        )
                    else:
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={
                                "s3:shape": asset_shape_list,
                                "s3:spatial_resolution": asset_resolution,
                            },
                        )
                    asset_identifier_list.append(asset_key)
                    asset_list.append(asset_obj)
            else:
                asset_key_list = constants.SYNERGY_VGP_ASSET_KEYS
                for ind, asset_key in enumerate(asset_key_list):
                    band_dict_list = []
                    if ind < 4:
                        band_key = list(constants.SENTINEL_SYNERGY_BANDS.keys())[-4:][
                            ind
                        ]
                        band_dict = {
                            "name": instrument_bands[band_key].name,
                            "description": instrument_bands[band_key].description,
                            "center_wavelength": instrument_bands[
                                band_key
                            ].center_wavelength,
                            "band_width": instrument_bands[
                                band_key
                            ].full_width_half_max,
                        }
                        band_dict_list.append(band_dict)
                    else:
                        band_dict_list = []
                    asset_location = self.read_href(
                        f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_href = os.path.join(self.granule_href, asset_location)
                    media_type = manifest.find_attr(
                        "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                    )
                    asset_description = manifest.find_attr(
                        "textInfo", f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_resolution = self._get_resolution(asset_href, skip_nc)
                    if skip_nc:
                        asset_shape_list = []
                    else:
                        asset_shape_list = []
                        ds = nc.Dataset(asset_href)
                        for key in ds.dimensions.keys():
                            asset_shape_dict = {key: int(ds.dimensions[key].size)}
                            asset_shape_list.append(asset_shape_dict)
                        ds.close()
                    if band_dict_list:
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={
                                "s3:shape": asset_shape_list,
                                "s3:spatial_resolution": asset_resolution,
                                "eo:bands": band_dict_list,
                            },
                        )
                    else:
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={
                                "s3:shape": asset_shape_list,
                                "s3:spatial_resolution": asset_resolution,
                            },
                        )
                    asset_identifier_list.append(asset_key)
                    asset_list.append(asset_obj)
        elif instrument_bands == constants.SENTINEL_OLCI_BANDS:
            if "OL_1_" in product_type:
                asset_key_list = constants.OLCI_L1_ASSET_KEYS
                for asset_key, band in zip(asset_key_list, instrument_bands):
                    band_dict = {
                        "name": instrument_bands[band].name,
                        "description": instrument_bands[band].description,
                        "center_wavelength": instrument_bands[band].center_wavelength,
                        "band_width": instrument_bands[band].full_width_half_max,
                    }
                    asset_location = self.read_href(
                        f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_href = os.path.join(
                        self.granule_href, strip_prefix("./", asset_location)
                    )
                    media_type = manifest.find_attr(
                        "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                    )
                    asset_description = manifest.find_attr(
                        "textInfo", f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_resolution = self._get_resolution(asset_href, skip_nc)
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={
                            "s3:spatial_resolution": asset_resolution,
                            "eo:bands": [band_dict],
                        },
                    )
                    asset_identifier_list.append(asset_key)
                    asset_list.append(asset_obj)
            elif any(_str in product_type for _str in ["_LFR_", "_LRR_"]):
                if len(manifest.findall(".//dataObject[@ID='ogviData']")) == 0:
                    asset_key_list = constants.OLCI_L2_LAND_ASSET_KEYS_RENAMED
                else:
                    asset_key_list = constants.OLCI_L2_LAND_ASSET_KEYS
                for asset_key in asset_key_list:
                    if asset_key == "ogviData" or asset_key == "gifaparData":
                        band_key_list = ["Oa03", "Oa10", "Oa17"]
                    elif asset_key == "otciData":
                        band_key_list = ["Oa10", "Oa11", "Oa12"]
                    elif asset_key == "iwvData":
                        band_key_list = ["Oa18", "Oa19"]
                    elif asset_key == "rcOgviData":
                        band_key_list = ["Oa10", "Oa17"]
                    else:
                        band_key_list = []
                    asset_location = self.read_href(
                        f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_href = os.path.join(
                        self.granule_href, strip_prefix("./", asset_location)
                    )
                    media_type = manifest.find_attr(
                        "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                    )
                    asset_description = manifest.find_attr(
                        "textInfo", f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_resolution = self._get_resolution(asset_href, skip_nc)
                    if not band_key_list:
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={"s3:spatial_resolution": asset_resolution},
                        )
                    else:
                        band_dict_list = []
                        for band in band_key_list:
                            band_dict = {
                                "name": instrument_bands[band].name,
                                "description": instrument_bands[band].description,
                                "center_wavelength": instrument_bands[
                                    band
                                ].center_wavelength,
                                "band_width": instrument_bands[
                                    band
                                ].full_width_half_max,
                            }
                            band_dict_list.append(band_dict)
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={
                                "s3:spatial_resolution": asset_resolution,
                                "eo:bands": band_dict_list,
                            },
                        )
                    asset_identifier_list.append(asset_key)
                    asset_list.append(asset_obj)
            elif "_WFR_" in product_type:
                # Map each water data object ID to the OLCI bands it is
                # derived from. Data objects without an entry here (annotation
                # files, and the Collection 4 chlor_a/fluorescence/iop_lsd
                # products) carry no eo:bands.
                band_key_map = {
                    "chlNnData": [
                        "Oa01",
                        "Oa02",
                        "Oa03",
                        "Oa04",
                        "Oa05",
                        "Oa06",
                        "Oa07",
                        "Oa08",
                        "Oa09",
                        "Oa10",
                        "Oa11",
                        "Oa12",
                        "Oa16",
                        "Oa17",
                        "Oa18",
                        "Oa21",
                    ],
                    "tsmNnData": [
                        "Oa01",
                        "Oa02",
                        "Oa03",
                        "Oa04",
                        "Oa05",
                        "Oa06",
                        "Oa07",
                        "Oa08",
                        "Oa09",
                        "Oa10",
                        "Oa11",
                        "Oa12",
                        "Oa16",
                        "Oa17",
                        "Oa18",
                        "Oa21",
                    ],
                    "chlOc4meData": ["Oa03", "Oa04", "Oa05", "Oa06"],
                    "iopNnData": ["Oa01", "Oa12", "Oa16", "Oa17", "Oa21"],
                    "iwvData": ["Oa18", "Oa19"],
                    "trspData": ["Oa04", "Oa06"],
                    "wAerData": ["Oa05", "Oa06", "Oa17"],
                }
                # Iterate over both the legacy water keys and the Collection 4
                # (v4.01) additions. Data objects that are not present in this
                # particular manifest are skipped, so the same code handles
                # both the old and new processing baselines.
                present_asset_keys = []
                for asset_key in (
                    constants.OLCI_L2_WATER_ASSET_KEYS
                    + constants.OLCI_L2_WATER_ASSET_KEYS_C4
                ):
                    if len(manifest.findall(f".//dataObject[@ID='{asset_key}']")) == 0:
                        continue
                    if asset_key in band_key_map:
                        band_key_list = band_key_map[asset_key]
                    elif asset_key.startswith("Oa") and asset_key.endswith(
                        "_reflectanceData"
                    ):
                        band_key_list = [asset_key[:4]]
                    else:
                        band_key_list = []
                    asset_location = self.read_href(
                        f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_href = os.path.join(
                        self.granule_href, strip_prefix("./", asset_location)
                    )
                    media_type = manifest.find_attr(
                        "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                    )
                    asset_description = manifest.find_attr(
                        "textInfo", f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_resolution = self._get_resolution(asset_href, skip_nc)
                    if band_key_list:
                        band_dict_list = []
                        for band in band_key_list:
                            band_dict = {
                                "name": instrument_bands[band].name,
                                "description": instrument_bands[band].description,
                                "center_wavelength": instrument_bands[
                                    band
                                ].center_wavelength,
                                "band_width": instrument_bands[
                                    band
                                ].full_width_half_max,
                            }
                            band_dict_list.append(band_dict)
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={
                                "s3:spatial_resolution": asset_resolution,
                                "eo:bands": band_dict_list,
                            },
                        )
                    else:
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={"s3:spatial_resolution": asset_resolution},
                        )
                    present_asset_keys.append(asset_key)
                    asset_identifier_list.append(asset_key)
                    asset_list.append(asset_obj)
                # Return only the keys actually present in this manifest so the
                # asset keys stay aligned with asset_identifier_list/asset_list.
                asset_key_list = present_asset_keys
        elif instrument_bands == constants.SENTINEL_SLSTR_BANDS:
            if "SL_1_" in product_type:
                asset_key_list = constants.SLSTR_L1_ASSET_KEYS
                for asset_key, band in zip(asset_key_list, instrument_bands):
                    band_dict = {
                        "name": instrument_bands[band].name,
                        "description": instrument_bands[band].description,
                        "center_wavelength": instrument_bands[band].center_wavelength,
                        "band_width": instrument_bands[band].full_width_half_max,
                    }
                    asset_location = self.read_href(
                        f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_href = os.path.join(
                        self.granule_href, strip_prefix("./", asset_location)
                    )
                    media_type = manifest.find_attr(
                        "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                    )
                    asset_description = manifest.find_attr(
                        "textInfo", f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_resolution = self._get_resolution(asset_href, skip_nc)
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={
                            "s3:spatial_resolution": asset_resolution,
                            "eo:bands": [band_dict],
                        },
                    )
                    asset_identifier_list.append(asset_key)
                    asset_list.append(asset_obj)
            elif "_FRP_" in product_type:
                asset_key_list = constants.SLSTR_L2_FRP_KEYS
                for asset_key in asset_key_list:
                    if asset_key == "FRP_IN_Data":
                        band_key_list = ["S05", "S06", "S07", "S10"]
                    else:
                        band_key_list = []
                    asset_location = self.read_href(
                        f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_href = os.path.join(
                        self.granule_href, strip_prefix("./", asset_location)
                    )
                    media_type = manifest.find_attr(
                        "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                    )
                    asset_description = manifest.find_attr(
                        "textInfo", f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_resolution = self._get_resolution(asset_href, skip_nc)
                    if band_key_list:
                        band_dict_list = []
                        for band in band_key_list:
                            band_dict = {
                                "name": instrument_bands[band].name,
                                "description": instrument_bands[band].description,
                                "center_wavelength": instrument_bands[
                                    band
                                ].center_wavelength,
                                "band_width": instrument_bands[
                                    band
                                ].full_width_half_max,
                            }
                            band_dict_list.append(band_dict)
                        asset_description = "Fire Radiative Power (FRP) dataset"
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={
                                "s3:spatial_resolution": asset_resolution,
                                "eo:bands": band_dict_list,
                            },
                        )
                    else:
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={"s3:spatial_resolution": asset_resolution},
                        )
                    asset_identifier_list.append(asset_key)
                    asset_list.append(asset_obj)
            elif "_LST_" in product_type:
                asset_key_list = constants.SLSTR_L2_LST_KEYS
                for asset_key in asset_key_list:
                    if asset_key == "LST_IN_Data":
                        band_key_list = ["S08", "S09"]
                    else:
                        band_key_list = []
                    asset_location = self.read_href(
                        f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_href = os.path.join(
                        self.granule_href, strip_prefix("./", asset_location)
                    )
                    media_type = manifest.find_attr(
                        "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                    )
                    asset_resolution = self._get_resolution(asset_href, skip_nc)
                    if band_key_list:
                        band_dict_list = []
                        for band in band_key_list:
                            band_dict = {
                                "name": instrument_bands[band].name,
                                "description": instrument_bands[band].description,
                                "center_wavelength": instrument_bands[
                                    band
                                ].center_wavelength,
                                "band_width": instrument_bands[
                                    band
                                ].full_width_half_max,
                            }
                            band_dict_list.append(band_dict)
                        asset_description = "Land Surface Temperature (LST) values"
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={
                                "s3:spatial_resolution": asset_resolution,
                                "eo:bands": band_dict_list,
                            },
                        )
                    else:
                        asset_description = manifest.find_attr(
                            "textInfo",
                            f".//dataObject[@ID='{asset_key}']//fileLocation",
                        )
                        asset_obj = pystac.Asset(
                            href=asset_href,
                            media_type=media_type,
                            description=asset_description,
                            roles=["data"],
                            extra_fields={"s3:spatial_resolution": asset_resolution},
                        )
                    asset_identifier_list.append(asset_key)
                    asset_list.append(asset_obj)
            elif "_WST_" in product_type:
                asset_key_list = ["L2P_Data"]
                band_key_list = ["S07", "S08", "S09"]
                band_dict_list = []
                for asset_key in asset_key_list:
                    for band in band_key_list:
                        band_dict = {
                            "name": instrument_bands[band].name,
                            "description": instrument_bands[band].description,
                            "center_wavelength": instrument_bands[
                                band
                            ].center_wavelength,
                            "band_width": instrument_bands[band].full_width_half_max,
                        }
                        band_dict_list.append(band_dict)
                    asset_location = self.read_href(
                        f".//dataObject[@ID='{asset_key}']//fileLocation"
                    )
                    asset_href = os.path.join(
                        self.granule_href, strip_prefix("./", asset_location)
                    )
                    media_type = manifest.find_attr(
                        "mimeType", f".//dataObject[@ID='{asset_key}']//byteStream"
                    )
                    asset_description = (
                        "Data respects the Group for High Resolution "
                        "Sea Surface Temperature (GHRSST) L2P specification"
                    )
                    asset_resolution = self._get_resolution(asset_href, skip_nc)
                    asset_obj = pystac.Asset(
                        href=asset_href,
                        media_type=media_type,
                        description=asset_description,
                        roles=["data"],
                        extra_fields={
                            "s3:spatial_resolution": asset_resolution,
                            "eo:bands": band_dict_list,
                        },
                    )
                    asset_identifier_list.append(asset_key)
                    asset_list.append(asset_obj)
        return asset_key_list, asset_identifier_list, asset_list
