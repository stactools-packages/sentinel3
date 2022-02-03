import os
from datetime import datetime
from typing import Any, Dict, Optional

from pystac.utils import str_to_datetime
from shapely.geometry import Polygon, mapping  # type: ignore
from stactools.core.io.xml import XmlElement

from stactools.sentinel3.constants import MANIFEST_FILENAME


class ProductMetadataError(Exception):
    pass


class ProductMetadata:

    def __init__(self, granule_href: str, manifest: XmlElement) -> None:
        self.granule_href = granule_href
        self.manifest_href = os.path.join(granule_href, MANIFEST_FILENAME)
        self._root = manifest

        def _get_geometries():
            # Find the footprint descriptor
            footprint_text = self._root.findall(".//gml:posList")
            if footprint_text is None:
                ProductMetadataError(
                    f"Cannot parse footprint from product metadata at {self.manifest_href}"
                )
            # Convert to values
            footprint_value = [
                float(x)
                for x in footprint_text[0].text.replace(" ", ",").split(",")
            ]

            footprint_points = [
                p[::-1] for p in list(zip(*[iter(footprint_value)] * 2))
            ]

            footprint_polygon = Polygon(footprint_points)
            geometry = mapping(footprint_polygon)
            bbox = list(footprint_polygon.bounds)

            return (bbox, geometry)

        self.bbox, self.geometry = _get_geometries()

    @property
    def scene_id(self) -> str:
        """Returns the string to be used for a STAC Item id.

        Removes the processing number and .SAFE extension
        from the product_id defined below.

        Parsed based on the naming convention found here:
        https://sentinel.esa.int/web/sentinel/user-guides/sentinel-3-slstr/naming-convention
        """
        product_id = self.product_id
        # Ensure the product id is as expected.
        if not product_id.endswith(".SEN3"):
            raise ValueError("Unexpected value found at "
                             f"{product_id}: "
                             "this was expected to follow the sentinel 3 "
                             "naming convention, including "
                             "ending in .SEN3")

        scene_id = self.product_id.split(".")[0]

        return scene_id

    @property
    def product_id(self) -> str:
        # Parse the name from href as it doesn't exist in xml files
        href = self.manifest_href
        result = href.split("/")[-2]
        if result is None:
            raise ValueError(
                "Cannot determine product ID using product metadata "
                f"at {self.manifest_href}")
        else:
            return result

    @property
    def get_datetime(self) -> datetime:
        start_time = self._root.findall(".//sentinel-safe:startTime")[0].text
        end_time = self._root.findall(".//sentinel-safe:stopTime")[0].text

        central_time = (
            datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ") +
            (datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%fZ") -
             datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ")) / 2)

        if central_time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.manifest_href}")
        else:
            return str_to_datetime(str(central_time))

    @property
    def start_datetime(self) -> datetime:
        time = self._root.findall(".//sentinel-safe:startTime")

        if time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.manifest_href}")
        else:
            return str_to_datetime(time[0].text)

    @property
    def end_datetime(self) -> datetime:
        time = self._root.findall(".//sentinel-safe:stopTime")

        if time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.manifest_href}")
        else:
            return str_to_datetime(time[0].text)

    @property
    def platform(self) -> Optional[str]:

        family_name = self._root.findall(".//sentinel-safe:familyName")[0].text
        platform_name = self._root.findall(".//sentinel-safe:number")[0].text

        return family_name + platform_name

    @property
    def cycle_number(self) -> Optional[str]:

        return self._root.findall(".//safe:cycleNumber")[0].text

    @property
    def metadata_dict(self) -> Dict[str, Any]:

        def _get_shape():
            x_size = int(self._root.findall(".//sentinel3:columns")[0].text)
            y_size = int(self._root.findall(".//sentinel3:rows")[0].text)
            shape = [x_size, y_size]

            return shape

        product_type = self._root.findall(".//sentinel3:productType")[0].text
        if (product_type.split("_")[0] == "OL"
                and product_type.split("_")[1] == "1"):
            result = {
                "start_datetime":
                str(self.start_datetime),
                "end_datetime":
                str(self.end_datetime),
                "instruments": [
                    str(
                        self._root.find_attr(
                            "abbreviation",
                            ".//sentinel-safe:familyName[@abbreviation]"))
                ],
                "s3:mode":
                str(self._root.find_attr("identifier",
                                         ".//sentinel-safe:mode")),
                "s3:productType":
                self._root.findall(".//sentinel3:productType")[0].text,
                "s3:gsd":
                300,
                "s3:salineWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage", ".//sentinel3:salineWaterPixels"))),
                "s3:coastalPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:coastalPixels"))),
                "s3:freshInlandWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//sentinel3:freshInlandWaterPixels"))),
                "s3:tidalRegionPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage", ".//sentinel3:tidalRegionPixels"))),
                "s3:brightPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:brightPixels"))),
                "s3:invalidPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//olci:invalidPixels"))),
                "s3:cosmeticPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//olci:cosmeticPixels"))),
                "s3:duplicatedPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//olci:duplicatedPixels"))),
                "s3:saturatedPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//olci:saturatedPixels"))),
                "s3:dubiousSamples_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//olci:dubiousSamples"))),
                "s3:shape":
                _get_shape()
            }
        elif (product_type.split("_")[0] == "OL"
              and product_type.split("_")[1] == "2"):
            result = {
                "start_datetime":
                str(self.start_datetime),
                "end_datetime":
                str(self.end_datetime),
                "instruments": [
                    str(
                        self._root.find_attr(
                            "abbreviation",
                            ".//sentinel-safe:familyName[@abbreviation]"))
                ],
                "s3:mode":
                str(self._root.find_attr("identifier",
                                         ".//sentinel-safe:mode")),
                "s3:productType":
                self._root.findall(".//sentinel3:productType")[0].text,
                "s3:gsd":
                300,
                "s3:salineWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage", ".//sentinel3:salineWaterPixels"))),
                "s3:coastalPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:coastalPixels"))),
                "s3:freshInlandWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//sentinel3:freshInlandWaterPixels"))),
                "s3:tidalRegionPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage", ".//sentinel3:tidalRegionPixels"))),
                "s3:landPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:landPixels"))),
                "s3:invalidPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//olci:invalidPixels"))),
                "s3:cosmeticPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//olci:cosmeticPixels"))),
                "s3:duplicatedPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//olci:duplicatedPixels"))),
                "s3:saturatedPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//olci:saturatedPixels"))),
                "s3:dubiousSamples_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//olci:dubiousSamples"))),
                "s3:shape":
                _get_shape()
            }
        elif (product_type.split("_")[0] == "SL"
              and product_type.split("_")[1] == "1"):
            result = {
                "start_datetime":
                str(self.start_datetime),
                "end_datetime":
                str(self.end_datetime),
                "instruments": [
                    str(
                        self._root.find_attr(
                            "abbreviation",
                            ".//sentinel-safe:familyName[@abbreviation]"))
                ],
                "s3:mode":
                str(self._root.find_attr("identifier",
                                         ".//sentinel-safe:mode")),
                "s3:productType":
                self._root.findall(".//sentinel3:productType")[0].text,
                "s3:gsd": {
                    "S1-S6": 500,
                    "S7-S9 and F1-F2": 1000
                },
                "s3:salineWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//slstr:classificationSummary[@grid='1 km']"
                            "/sentinel3:salineWaterPixels"))),
                "s3:landPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//slstr:classificationSummary[@grid='1 km']"
                            "/sentinel3:landPixels"))),
                "s3:coastalPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//slstr:classificationSummary[@grid='1 km']"
                            "/sentinel3:coastalPixels"))),
                "s3:freshInlandWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//slstr:classificationSummary[@grid='1 km']"
                            "/sentinel3:freshInlandWaterPixels"))),
                "s3:tidalRegionPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//slstr:classificationSummary[@grid='1 km']"
                            "/sentinel3:tidalRegionPixels"))),
                "s3:cosmeticPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//slstr:pixelQualitySummary[@grid='1 km']"
                            "/slstr:cosmeticPixels"))),
                "s3:duplicatedPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//slstr:pixelQualitySummary[@grid='1 km']"
                            "/slstr:duplicatedPixels"))),
                "s3:saturatedPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//slstr:pixelQualitySummary[@grid='1 km']"
                            "/slstr:saturatedPixels"))),
                "s3:outOfRangePixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//slstr:pixelQualitySummary[@grid='1 km']"
                            "/slstr:outOfRangePixels"))),
                "s3:shape":
                _get_shape()
            }
        elif (product_type.split("_")[0] == "SL"
              and product_type.split("_")[1] == "2"):
            result = {
                "start_datetime":
                str(self.start_datetime),
                "end_datetime":
                str(self.end_datetime),
                "instruments": [
                    str(
                        self._root.find_attr(
                            "abbreviation",
                            ".//sentinel-safe:familyName[@abbreviation]"))
                ],
                "s3:mode":
                str(self._root.find_attr("identifier",
                                         ".//sentinel-safe:mode")),
                "s3:productType":
                self._root.findall(".//sentinel3:productType")[0].text,
                "s3:gsd": {
                    "S1-S6": 500,
                    "S7-S9 and F1-F2": 1000
                },
                "s3:salineWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage", ".//sentinel3:salineWaterPixels"))),
                "s3:landPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:landPixels"))),
                "s3:coastalPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:coastalPixels"))),
                "s3:freshInlandWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//sentinel3:freshInlandWaterPixels"))),
                "s3:tidalRegionPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage", ".//sentinel3:tidalRegionPixels"))),
                "s3:cosmeticPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//slstr:cosmeticPixels"))),
                "s3:duplicatedPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//slstr:duplicatedPixels"))),
                "s3:saturatedPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//slstr:saturatedPixels"))),
                "s3:outOfRangePixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//slstr:outOfRangePixels"))),
                "s3:shape":
                _get_shape()
            }
        elif (product_type.split("_")[0] == "SR"
              and product_type.split("_")[1] == "2"):
            result = {
                "start_datetime":
                str(self.start_datetime),
                "end_datetime":
                str(self.end_datetime),
                "instruments": [
                    str(
                        self._root.find_attr(
                            "abbreviation",
                            ".//sentinel-safe:familyName[@abbreviation]"))
                ],
                "s3:mode":
                str(self._root.find_attr("identifier",
                                         ".//sentinel-safe:mode")),
                "s3:productType":
                self._root.findall(".//sentinel3:productType")[0].text,
                "s3:gsd": {
                    "along-track": 300,
                    "across-track": 1640
                },
                "s3:lrmModePercentage":
                float(self._root.findall(".//sral:lrmModePercentage")[0].text),
                "s3:sarModePercentage":
                float(self._root.findall(".//sral:sarModePercentage")[0].text),
                "s3:landPercentage":
                float(self._root.findall(".//sral:landPercentage")[0].text),
                "s3:closedSeaPercentage":
                float(
                    self._root.findall(".//sral:closedSeaPercentage")[0].text),
                "s3:continentalIcePercentage":
                float(
                    self._root.findall(".//sral:continentalIcePercentage")
                    [0].text),
                "s3:openOceanPercentage":
                float(
                    self._root.findall(".//sral:openOceanPercentage")[0].text),
            }
        elif "SY_2_AOD" in product_type:
            result = {
                "start_datetime":
                str(self.start_datetime),
                "end_datetime":
                str(self.end_datetime),
                "instruments": [
                    str(
                        self._root.find_attr(
                            "abbreviation",
                            ".//sentinel-safe:familyName[@abbreviation]"))
                ],
                "s3:mode":
                str(self._root.find_attr("identifier",
                                         ".//sentinel-safe:mode")),
                "s3:productType":
                self._root.findall(".//sentinel3:productType")[0].text,
                "s3:gsd": {
                    "OLCI": 300,
                    "SLSTR": {
                        "S1-S6": 500,
                        "S7-S9 and F1-F2": 1000
                    }
                },
                "s3:salineWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage", ".//sentinel3:salineWaterPixels"))),
                "s3:landPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:landPixels"))),
                "s3:shape":
                _get_shape()
            }
        elif "SY_2_SYN" in product_type:
            result = {
                "start_datetime":
                str(self.start_datetime),
                "end_datetime":
                str(self.end_datetime),
                "instruments": [
                    str(
                        self._root.find_attr(
                            "abbreviation",
                            ".//sentinel-safe:familyName[@abbreviation]"))
                ],
                "s3:mode":
                str(self._root.find_attr("identifier",
                                         ".//sentinel-safe:mode")),
                "s3:productType":
                self._root.findall(".//sentinel3:productType")[0].text,
                "s3:gsd": {
                    "OLCI": 300,
                    "SLSTR": {
                        "S1-S6": 500,
                        "S7-S9 and F1-F2": 1000
                    }
                },
                "s3:salineWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage", ".//sentinel3:salineWaterPixels"))),
                "s3:coastalPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:coastalPixels"))),
                "s3:freshInlandWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//sentinel3:freshInlandWaterPixels"))),
                "s3:tidalRegionPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage", ".//sentinel3:tidalRegionPixels"))),
                "s3:landPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:landPixels"))),
            }
        elif "SY_2_V10" in product_type:
            result = {
                "start_datetime":
                str(self.start_datetime),
                "end_datetime":
                str(self.end_datetime),
                "instruments": [
                    str(
                        self._root.find_attr(
                            "abbreviation",
                            ".//sentinel-safe:familyName[@abbreviation]"))
                ],
                "s3:mode":
                str(self._root.find_attr("identifier",
                                         ".//sentinel-safe:mode")),
                "s3:productType":
                self._root.findall(".//sentinel3:productType")[0].text,
                "s3:gsd": {
                    "OLCI": 300,
                    "SLSTR": {
                        "S1-S6": 500,
                        "S7-S9 and F1-F2": 1000
                    }
                },
                "s3:snowOrIcePixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:snowOrIcePixels"))),
                "s3:landPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:landPixels"))),
            }
        elif "SY_2_VG1" in product_type:
            result = {
                "start_datetime":
                str(self.start_datetime),
                "end_datetime":
                str(self.end_datetime),
                "instruments": [
                    str(
                        self._root.find_attr(
                            "abbreviation",
                            ".//sentinel-safe:familyName[@abbreviation]"))
                ],
                "s3:mode":
                str(self._root.find_attr("identifier",
                                         ".//sentinel-safe:mode")),
                "s3:productType":
                self._root.findall(".//sentinel3:productType")[0].text,
                "s3:gsd": {
                    "OLCI": 300,
                    "SLSTR": {
                        "S1-S6": 500,
                        "S7-S9 and F1-F2": 1000
                    }
                },
                "s3:snowOrIcePixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:snowOrIcePixels"))),
                "s3:landPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:landPixels"))),
            }
        elif "SY_2_VGP" in product_type:
            result = {
                "start_datetime":
                str(self.start_datetime),
                "end_datetime":
                str(self.end_datetime),
                "instruments": [
                    str(
                        self._root.find_attr(
                            "abbreviation",
                            ".//sentinel-safe:familyName[@abbreviation]"))
                ],
                "s3:mode":
                str(self._root.find_attr("identifier",
                                         ".//sentinel-safe:mode")),
                "s3:productType":
                self._root.findall(".//sentinel3:productType")[0].text,
                "s3:gsd": {
                    "OLCI": 300,
                    "SLSTR": {
                        "S1-S6": 500,
                        "S7-S9 and F1-F2": 1000
                    }
                },
                "s3:snowOrIcePixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:snowOrIcePixels"))),
                "s3:salineWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage", ".//sentinel3:salineWaterPixels"))),
                "s3:coastalPixelss_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:coastalPixels"))),
                "s3:freshInlandWaterPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage",
                            ".//sentinel3:freshInlandWaterPixels"))),
                "s3:tidalRegionPixels_percentage":
                float(
                    str(
                        self._root.find_attr(
                            "percentage", ".//sentinel3:tidalRegionPixels"))),
                "s3:landPixels_percentage":
                float(
                    str(
                        self._root.find_attr("percentage",
                                             ".//sentinel3:landPixels"))),
            }
        else:
            raise RuntimeError(
                f"Unsupported product type encountered: {product_type}")

        return {k: v for k, v in result.items() if v is not None}

    @property
    def get_epsg(self):
        epsg = self._root.find_attr(
            "srsName", ".//sentinel-safe:footPrint").split("/")[-1]

        return int(epsg)
