import unittest

import pystac
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.sat import SatExtension

from stactools.sentinel3.metadata_links import MetadataLinks
from stactools.sentinel3.product_metadata import ProductMetadata
from stactools.sentinel3.properties import (fill_proj_properties,
                                            fill_sat_properties)
from tests import test_data


class Sentinel3SLSTRMetadataTest(unittest.TestCase):
    def test_parses_product_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SL_1_RBT____20210827T074336_20210827T074636_20210827T094954_"
            "0179_075_320_3060_LN2_O_NR_004.SEN3")

        metalinks = MetadataLinks(manifest_path)

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

        # proj
        proj = ProjectionExtension.ext(item, add_if_missing=True)
        fill_proj_properties(proj, product_metadata)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "epsg":
            item.properties["proj:epsg"],
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "shape":
            item.properties["proj:shape"],
            "instrument":
            item.properties["s3:instrument"],
            "mode":
            item.properties["s3:mode"],
            "productType":
            item.properties["s3:productType"],
            "salineWaterPixels_percentage":
            item.properties["s3:salineWaterPixels_percentage"],
            "landPixels_percentage":
            item.properties["s3:landPixels_percentage"],
            "coastalPixels_percentage":
            item.properties["s3:coastalPixels_percentage"],
            "freshInlandWaterPixels_percentage":
            item.properties["s3:freshInlandWaterPixels_percentage"],
            "tidalRegionPixels_percentage":
            item.properties["s3:tidalRegionPixels_percentage"],
            "cosmeticPixels_percentage":
            item.properties["s3:cosmeticPixels_percentage"],
            "duplicatedPixels_percentage":
            item.properties["s3:duplicatedPixels_percentage"],
            "saturatedPixels_percentage":
            item.properties["s3:saturatedPixels_percentage"],
            "outOfRangePixels_percentage":
            item.properties["s3:outOfRangePixels_percentage"],
        }

        expected = {
            "bbox": [22.5729, -13.6378, 38.2488, -0.086826],
            "epsg": 4326,
            "datetime": "2021-08-27T07:45:05.980881Z",
            "orbit_state": "descending",
            "absolute_orbit": 28783,
            "relative_orbit": 320,
            "shape": [1500, 1200],
            "instrument": "SLSTR",
            "mode": "EO",
            "productType": "SL_1_RBT___",
            "salineWaterPixels_percentage": 0.0,
            "landPixels_percentage": 100.0,
            "coastalPixels_percentage": 0.0,
            "freshInlandWaterPixels_percentage": 6.677569,
            "tidalRegionPixels_percentage": 0.0,
            "cosmeticPixels_percentage": 27.02875,
            "duplicatedPixels_percentage": 5.058438,
            "saturatedPixels_percentage": 0.0,
            "outOfRangePixels_percentage": 14.225087,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)
