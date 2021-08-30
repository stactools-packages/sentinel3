from datetime import datetime
import os
from typing import Any, Dict, Optional, List

from shapely.geometry import mapping, Polygon  # type: ignore
from pystac.utils import str_to_datetime

from stactools.core.io.xml import XmlElement


class ProductMetadataError(Exception):
    pass


class ProductMetadata:
    def __init__(
        self,
        href,
    ) -> None:
        self.href = href
        self._root = XmlElement.from_file(href)

        def _get_geometries():
            # Find the footprint descriptor
            footprint_text = self._root.findall(".//gml:posList")
            if footprint_text is None:
                ProductMetadataError(
                    f"Cannot parse footprint from product metadata at {self.href}"
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
            bbox = footprint_polygon.bounds

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
        href = self.href
        result = href.split("/")[-2]
        if result is None:
            raise ValueError(
                "Cannot determine product ID using product metadata "
                f"at {self.href}")
        else:
            return result

    @property
    def get_datetime(self) -> datetime:
        start_time = self._root.findall(".//sentinel3:receivingStartTime")[0].text
        end_time = self._root.findall(".//sentinel3:receivingStopTime")[0].text

        central_time = (
            datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ") +
            (datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S.%fZ") -
             datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ")) / 2)

        if central_time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}")
        else:
            return str_to_datetime(str(central_time))

    @property
    def start_datetime(self) -> datetime:
        time = self._root.findall(".//sentinel3:receivingStartTime")

        if time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}")
        else:
            return str_to_datetime(time[0].text)

    @property
    def end_datetime(self) -> datetime:
        time = self._root.findall(".//sentinel3:receivingStopTime")

        if time is None:
            raise ValueError(
                "Cannot determine product start time using product metadata "
                f"at {self.href}")
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
    def image_paths(self) -> List[str]:
        head_folder = os.path.dirname(self.href)
        measurements = os.path.join(head_folder, "measurement")
        return [x for x in os.listdir(measurements) if x.endswith("tiff")]

    @property
    def metadata_dict(self) -> Dict[str, Any]:
        result = {
            "start_datetime":
            str(self.start_datetime),
            "end_datetime":
            str(self.end_datetime),
#             "s1:instrument_configuration_ID":
#             self._root.findall(".//s1sarl1:instrumentConfigurationID")[0].text,
#             "s1:datatake_id":
#             self._root.findall(".//s1sarl1:missionDataTakeID")[0].text,
        }

        return {k: v for k, v in result.items() if v is not None}
