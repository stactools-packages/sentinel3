import unittest

import pystac
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.sat import SatExtension

from stactools.sentinel3.metadata_links import MetadataLinks
from stactools.sentinel3.product_metadata import ProductMetadata
from stactools.sentinel3.properties import (fill_proj_properties,
                                            fill_sat_properties)
from tests import test_data


class Sentinel3OLCIMetadataTest(unittest.TestCase):
    def test_parses_product_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_OL_1_EFR____20210820T103153_20210820T103453_20210820T124206_"
            "0179_075_222_2160_LN1_O_NR_002.SEN3")

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
            "coastalPixels_percentage":
            item.properties["s3:coastalPixels_percentage"],
            "freshInlandWaterPixels_percentage":
            item.properties["s3:freshInlandWaterPixels_percentage"],
            "tidalRegionPixels_percentage":
            item.properties["s3:tidalRegionPixels_percentage"],
            "brightPixels_percentage":
            item.properties["s3:brightPixels_percentage"],
            "invalidPixels_percentage":
            item.properties["s3:invalidPixels_percentage"],
            "cosmeticPixels_percentage":
            item.properties["s3:cosmeticPixels_percentage"],
            "duplicatedPixels_percentage":
            item.properties["s3:duplicatedPixels_percentage"],
            "saturatedPixels_percentage":
            item.properties["s3:saturatedPixels_percentage"],
            "dubiousSamples_percentage":
            item.properties["s3:dubiousSamples_percentage"],
        }

        expected = {
            "bbox": [-12.7336, 39.5443, 7.26622, 52.4486],
            "epsg": 4326,
            "datetime": "2021-08-20T10:33:22.751633Z",
            "orbit_state": "descending",
            "absolute_orbit": 28685,
            "relative_orbit": 222,
            "shape": [4865, 4090],
            "instrument": "OLCI",
            "mode": "EO",
            "productType": "OL_1_EFR___",
            "salineWaterPixels_percentage": 52.0,
            "coastalPixels_percentage": 0.0,
            "freshInlandWaterPixels_percentage": 0.0,
            "tidalRegionPixels_percentage": 2.0,
            "brightPixels_percentage": 45.0,
            "invalidPixels_percentage": 4.0,
            "cosmeticPixels_percentage": 0.0,
            "duplicatedPixels_percentage": 23.0,
            "saturatedPixels_percentage": 6e-06,
            "dubiousSamples_percentage": 0.0,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)
