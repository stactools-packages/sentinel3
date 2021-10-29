import unittest

import pystac
from pystac.extensions.eo import EOExtension
from pystac.extensions.sat import SatExtension

from stactools.sentinel3.metadata_links import MetadataLinks
from stactools.sentinel3.product_metadata import ProductMetadata
from stactools.sentinel3.properties import (fill_eo_properties,
                                            fill_sat_properties)
from tests import test_data


class Sentinel3OLCIMetadataTest(unittest.TestCase):
    def test_parses_olci_1_efr_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_OL_1_EFR____20211021T073827_20211021T074112_20211021T091357_"
            "0164_077_334_4320_LN1_O_NR_002.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
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
            "shape":
            item.properties["s3:shape"]
        }

        expected = {
            "bbox": [-44.0441, -83.51, 13.0151, -68.2251],
            "datetime": "2021-10-21T07:39:49.724590Z",
            "orbit_state": "descending",
            "absolute_orbit": 29567,
            "relative_orbit": 334,
            "instrument": "OLCI",
            "mode": "EO",
            "productType": "OL_1_EFR___",
            "salineWaterPixels_percentage": 44.0,
            "coastalPixels_percentage": 0.0,
            "freshInlandWaterPixels_percentage": 0.0,
            "tidalRegionPixels_percentage": 0.0,
            "brightPixels_percentage": 99.0,
            "invalidPixels_percentage": 1.0,
            "cosmeticPixels_percentage": 0.0,
            "duplicatedPixels_percentage": 25.0,
            "saturatedPixels_percentage": 0.0,
            "dubiousSamples_percentage": 0.0,
            "shape": [4865, 3749]
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_olci_1_err_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3B_OL_1_ERR____20210831T200148_20210831T204600_20210902T011514_"
            "2652_056_242______LN1_O_NT_002.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
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
            "shape":
            item.properties["s3:shape"]
        }

        expected = {
            "bbox": [-179.151, -64.2325, 179.92, 89.5069],
            "datetime": "2021-08-31T20:23:54.000366Z",
            "orbit_state": "ascending",
            "absolute_orbit": 17454,
            "relative_orbit": 242,
            "instrument": "OLCI",
            "mode": "EO",
            "productType": "OL_1_ERR___",
            "salineWaterPixels_percentage": 90.0,
            "coastalPixels_percentage": 0.0,
            "freshInlandWaterPixels_percentage": 0.0,
            "tidalRegionPixels_percentage": 0.0,
            "brightPixels_percentage": 47.0,
            "invalidPixels_percentage": 3.0,
            "cosmeticPixels_percentage": 0.0,
            "duplicatedPixels_percentage": 0.0,
            "saturatedPixels_percentage": 8e-06,
            "dubiousSamples_percentage": 0.0,
            "shape": [1217, 15070]
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_olci_2_lfr_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_OL_2_LFR____20210523T003029_20210523T003329_20210524T050403_"
            "0179_072_102_1980_LN1_O_NT_002.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "landPixels_percentage":
            item.properties["s3:landPixels_percentage"],
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
            "shape":
            item.properties["s3:shape"]
        }

        expected = {
            "bbox": [138.497, 49.8938, 164.009, 62.918],
            "datetime": "2021-05-23T00:31:59.485583Z",
            "orbit_state": "descending",
            "absolute_orbit": 27410,
            "relative_orbit": 102,
            "cloud_cover": 83.0,
            "instrument": "OLCI",
            "mode": "EO",
            "productType": "OL_2_LFR___",
            "salineWaterPixels_percentage": 4.0,
            "coastalPixels_percentage": 0.0082,
            "freshInlandWaterPixels_percentage": 0.0,
            "tidalRegionPixels_percentage": 1.0,
            "landPixels_percentage": 4.0,
            "invalidPixels_percentage": 4.0,
            "cosmeticPixels_percentage": 0.0,
            "duplicatedPixels_percentage": 1.545942,
            "saturatedPixels_percentage": 0.0,
            "dubiousSamples_percentage": 0.0,
            "shape": [4865, 4090]
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_olci_2_lrr_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3B_OL_2_LRR____20210731T214325_20210731T222741_20210802T020007_"
            "2656_055_186______LN1_O_NT_002.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "landPixels_percentage":
            item.properties["s3:landPixels_percentage"],
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
            "shape":
            item.properties["s3:shape"]
        }

        expected = {
            "bbox": [-179.968, -53.7609, 179.943, 89.6231],
            "datetime": "2021-07-31T22:05:32.974566Z",
            "orbit_state": "ascending",
            "absolute_orbit": 17013,
            "relative_orbit": 186,
            "cloud_cover": 51.0,
            "instrument": "OLCI",
            "mode": "EO",
            "productType": "OL_2_LRR___",
            "salineWaterPixels_percentage": 35.0,
            "coastalPixels_percentage": 0.332161,
            "freshInlandWaterPixels_percentage": 0.0,
            "tidalRegionPixels_percentage": 0.0,
            "landPixels_percentage": 1.0,
            "invalidPixels_percentage": 4.0,
            "cosmeticPixels_percentage": 0.0,
            "duplicatedPixels_percentage": 0.0,
            "saturatedPixels_percentage": 0.0,
            "dubiousSamples_percentage": 0.0,
            "shape": [1217, 15092]
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_olci_2_wfr_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_OL_2_WFR____20210604T001016_20210604T001316_20210604T021918_"
            "0179_072_273_1440_MAR_O_NR_003.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "landPixels_percentage":
            item.properties["s3:landPixels_percentage"],
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
            "shape":
            item.properties["s3:shape"]
        }

        expected = {
            "bbox": [-176.303, 76.7724, 179.972, 88.9826],
            "datetime": "2021-06-04T00:11:45.867265Z",
            "orbit_state": "ascending",
            "absolute_orbit": 27581,
            "relative_orbit": 273,
            "cloud_cover": 67.0,
            "instrument": "OLCI",
            "mode": "EO",
            "productType": "OL_2_WFR___",
            "salineWaterPixels_percentage": 0.0,
            "coastalPixels_percentage": 0.013921,
            "freshInlandWaterPixels_percentage": 0.0,
            "tidalRegionPixels_percentage": 0.0,
            "landPixels_percentage": 0.0,
            "invalidPixels_percentage": 3.0,
            "cosmeticPixels_percentage": 0.0,
            "duplicatedPixels_percentage": 11.701367,
            "saturatedPixels_percentage": 0.0,
            "dubiousSamples_percentage": 0.0,
            "shape": [4865, 4091]
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_slstr_1_rbt_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SL_1_RBT____20210930T220914_20210930T221214_20211002T102150_"
            "0180_077_043_5400_LN2_O_NT_004.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "shape":
            item.properties["s3:shape"]
        }

        expected = {
            "bbox": [-3.34105, -39.7421, 15.4906, -25.8488],
            "datetime": "2021-09-30T22:10:43.843538Z",
            "orbit_state": "ascending",
            "absolute_orbit": 29276,
            "relative_orbit": 43,
            "cloud_cover": 80.216007,
            "instrument": "SLSTR",
            "mode": "EO",
            "productType": "SL_1_RBT___",
            "salineWaterPixels_percentage": 100.0,
            "landPixels_percentage": 0.0,
            "coastalPixels_percentage": 0.0,
            "freshInlandWaterPixels_percentage": 0.0,
            "tidalRegionPixels_percentage": 0.0,
            "cosmeticPixels_percentage": 28.085521,
            "duplicatedPixels_percentage": 5.105382,
            "saturatedPixels_percentage": 0.0,
            "outOfRangePixels_percentage": 0.0,
            "shape": [1500, 1200]
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_slstr_2_frp_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SL_2_FRP____20210802T000420_20210802T000720_20210803T123912_"
            "0179_074_344_2880_LN2_O_NT_004.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "shape":
            item.properties["s3:shape"]
        }

        expected = {
            "bbox": [139.182, -3.03934, 154.722, 10.4264],
            "datetime": "2021-08-02T00:05:49.503088Z",
            "orbit_state": "descending",
            "absolute_orbit": 28422,
            "relative_orbit": 344,
            "cloud_cover": 63.904667,
            "instrument": "SLSTR",
            "mode": "EO",
            "productType": "SL_2_FRP___",
            "salineWaterPixels_percentage": 99.891,
            "landPixels_percentage": 0.109,
            "coastalPixels_percentage": 0.017944,
            "freshInlandWaterPixels_percentage": 0.000167,
            "tidalRegionPixels_percentage": 0.0,
            "cosmeticPixels_percentage": 21.585889,
            "duplicatedPixels_percentage": 5.461111,
            "saturatedPixels_percentage": 0.0,
            "outOfRangePixels_percentage": 0.184722,
            "shape": [1500, 1200]
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_slstr_2_lst_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SL_2_LST____20210510T002955_20210510T003255_20210511T101010_"
            "0179_071_301_5760_LN2_O_NT_004.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "shape":
            item.properties["s3:shape"]
        }

        expected = {
            "bbox": [-41.5076, -18.6129, -25.5773, -5.01269],
            "datetime": "2021-05-10T00:31:24.660731Z",
            "orbit_state": "ascending",
            "absolute_orbit": 27224,
            "relative_orbit": 301,
            "cloud_cover": 57.378222,
            "instrument": "SLSTR",
            "mode": "EO",
            "productType": "SL_2_LST___",
            "salineWaterPixels_percentage": 78.747222,
            "landPixels_percentage": 21.252778,
            "coastalPixels_percentage": 0.050167,
            "freshInlandWaterPixels_percentage": 0.169778,
            "tidalRegionPixels_percentage": 0.899167,
            "cosmeticPixels_percentage": 21.881167,
            "duplicatedPixels_percentage": 5.449222,
            "saturatedPixels_percentage": 0.0,
            "outOfRangePixels_percentage": 0.0,
            "shape": [1500, 1200]
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_slstr_2_wst_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3B_SL_2_WST____20210419T051754_20210419T065853_20210420T160434_"
            "6059_051_247______MAR_O_NT_003.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "shape":
            item.properties["s3:shape"]
        }

        expected = {
            "bbox": [-175.687, -85.8995, 175.031, 89.0613],
            "datetime": "2021-04-19T06:08:23.709828Z",
            "orbit_state": "descending",
            "absolute_orbit": 15534,
            "relative_orbit": 247,
            "cloud_cover": 67.421502,
            "instrument": "SLSTR",
            "mode": "EO",
            "productType": "SL_2_WST___",
            "salineWaterPixels_percentage": 69.464947,
            "landPixels_percentage": 30.535053,
            "coastalPixels_percentage": 0.0,
            "freshInlandWaterPixels_percentage": 0.0,
            "tidalRegionPixels_percentage": 0.0,
            "cosmeticPixels_percentage": 42.198716,
            "duplicatedPixels_percentage": 0.0,
            "saturatedPixels_percentage": 0.0,
            "outOfRangePixels_percentage": 26.93685,
            "shape": [1500, 40394]
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_sral_2_lan_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SR_2_LAN____20210611T011438_20210611T012436_20210611T024819_"
            "0598_072_373______LN3_O_NR_004.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "instrument":
            item.properties["s3:instrument"],
            "mode":
            item.properties["s3:mode"],
            "productType":
            item.properties["s3:productType"],
            "lrmModePercentage":
            item.properties["s3:lrmModePercentage"],
            "sarModePercentage":
            item.properties["s3:sarModePercentage"],
            "landPercentage":
            item.properties["s3:landPercentage"],
            "closedSeaPercentage":
            item.properties["s3:closedSeaPercentage"],
            "continentalIcePercentage":
            item.properties["s3:continentalIcePercentage"],
            "openOceanPercentage":
            item.properties["s3:openOceanPercentage"],
        }

        expected = {
            "bbox": [-19.9677, -81.3739, 110.573, -67.0245],
            "datetime": "2021-06-11T01:19:37.201974Z",
            "orbit_state": "descending",
            "absolute_orbit": 27681,
            "relative_orbit": 373,
            "instrument": "SRAL",
            "mode": "EO",
            "productType": "SR_2_LAN___",
            "lrmModePercentage": 0.0,
            "sarModePercentage": 100.0,
            "landPercentage": 0.0,
            "closedSeaPercentage": 0.0,
            "continentalIcePercentage": 97.0,
            "openOceanPercentage": 3.0,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_sral_2_wat_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SR_2_WAT____20210704T012815_20210704T021455_20210729T173140_"
            "2800_073_316______MAR_O_NT_004.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "instrument":
            item.properties["s3:instrument"],
            "mode":
            item.properties["s3:mode"],
            "productType":
            item.properties["s3:productType"],
            "lrmModePercentage":
            item.properties["s3:lrmModePercentage"],
            "sarModePercentage":
            item.properties["s3:sarModePercentage"],
            "landPercentage":
            item.properties["s3:landPercentage"],
            "closedSeaPercentage":
            item.properties["s3:closedSeaPercentage"],
            "continentalIcePercentage":
            item.properties["s3:continentalIcePercentage"],
            "openOceanPercentage":
            item.properties["s3:openOceanPercentage"],
        }

        expected = {
            "bbox": [-153.507, -74.0588, -20.0953, 81.4226],
            "datetime": "2021-07-04T01:51:35.180925Z",
            "orbit_state": "descending",
            "absolute_orbit": 28009,
            "relative_orbit": 316,
            "instrument": "SRAL",
            "mode": "EO",
            "productType": "SR_2_WAT___",
            "lrmModePercentage": 0.0,
            "sarModePercentage": 100.0,
            "landPercentage": 8.0,
            "closedSeaPercentage": 0.0,
            "continentalIcePercentage": 0.0,
            "openOceanPercentage": 92.0,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_synergy_2_aod_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3B_SY_2_AOD____20210512T143315_20210512T151738_20210514T064157_"
            "2663_052_196______LN2_O_NT_002.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "shape":
            item.properties["s3:shape"]
        }

        expected = {
            "bbox": [-104.241, -54.5223, 112.209, 89.7337],
            "datetime": "2021-05-12T14:55:26.593379Z",
            "orbit_state": "ascending",
            "absolute_orbit": 15868,
            "relative_orbit": 196,
            "cloud_cover": 82.147057,
            "instrument": "SYNERGY",
            "mode": "EO",
            "productType": "SY_2_AOD___",
            "salineWaterPixels_percentage": 72.660328,
            "landPixels_percentage": 27.276878,
            "shape": [324, 4035]
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_synergy_2_syn_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SY_2_SYN____20210325T005418_20210325T005718_20210325T142858_"
            "0180_070_031_1620_LN2_O_ST_002.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "landPixels_percentage":
            item.properties["s3:landPixels_percentage"]
        }

        expected = {
            "bbox": [-179.619, 69.3884, 179.853, 83.7777],
            "datetime": "2021-03-25T00:55:48.019583Z",
            "orbit_state": "descending",
            "absolute_orbit": 26569,
            "relative_orbit": 31,
            "cloud_cover": 8.166911,
            "instrument": "SYNERGY",
            "mode": "EO",
            "productType": "SY_2_SYN___",
            "salineWaterPixels_percentage": 94.483109,
            "coastalPixels_percentage": 0.093193,
            "freshInlandWaterPixels_percentage": 0.076276,
            "tidalRegionPixels_percentage": 0.0,
            "landPixels_percentage": 2.368632
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_synergy_2_v10_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SY_2_V10____20210911T000000_20210920T235959_20210928T121452_"
            "EUROPE____________LN2_O_NT_002.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
            "instrument":
            item.properties["s3:instrument"],
            "mode":
            item.properties["s3:mode"],
            "productType":
            item.properties["s3:productType"],
            "snowOrIcePixels_percentage":
            item.properties["s3:snowOrIcePixels_percentage"],
            "landPixels_percentage":
            item.properties["s3:landPixels_percentage"]
        }

        expected = {
            "bbox": [-10.9911, 25.0, 62.0, 75.0],
            "datetime": "2021-09-15T23:59:59.500000Z",
            "orbit_state": "descending",
            "absolute_orbit": 28848,
            "relative_orbit": 145,
            "cloud_cover": 3.041905,
            "instrument": "SYNERGY",
            "mode": "EO",
            "productType": "SY_2_V10___",
            "snowOrIcePixels_percentage": 0.154442,
            "landPixels_percentage": 65.278832
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_synergy_2_vg1_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SY_2_VG1____20211013T000000_20211013T235959_20211014T203456_"
            "EUROPE____________LN2_O_ST_002.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
            "instrument":
            item.properties["s3:instrument"],
            "mode":
            item.properties["s3:mode"],
            "productType":
            item.properties["s3:productType"],
            "snowOrIcePixels_percentage":
            item.properties["s3:snowOrIcePixels_percentage"],
            "landPixels_percentage":
            item.properties["s3:landPixels_percentage"]
        }

        expected = {
            "bbox": [-10.9911, 25.0, 62.0, 75.0],
            "datetime": "2021-10-13T11:59:59.500000Z",
            "orbit_state": "descending",
            "absolute_orbit": 29233,
            "relative_orbit": 216,
            "cloud_cover": 23.811417,
            "instrument": "SYNERGY",
            "mode": "EO",
            "productType": "SY_2_VG1___",
            "snowOrIcePixels_percentage": 0.102883,
            "landPixels_percentage": 46.680979
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_synergy_2_vgp_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SY_2_VGP____20210703T142237_20210703T150700_20210703T211742_"
            "2663_073_310______LN2_O_ST_002.SEN3")

        metalinks = MetadataLinks(manifest_path)

        product_metadata = ProductMetadata(manifest_path, metalinks.manifest)

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
        fill_sat_properties(sat, metalinks.manifest)

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.manifest)

        # s3 properties
        item.properties.update({**product_metadata.metadata_dict})

        # Make a dictionary of the properties
        s3_props = {
            "bbox":
            item.bbox,
            "datetime":
            item.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "orbit_state":
            item.properties["sat:orbit_state"],
            "absolute_orbit":
            item.properties["sat:absolute_orbit"],
            "relative_orbit":
            item.properties["sat:relative_orbit"],
            "cloud_cover":
            item.properties["eo:cloud_cover"],
            "instrument":
            item.properties["s3:instrument"],
            "mode":
            item.properties["s3:mode"],
            "productType":
            item.properties["s3:productType"],
            "snowOrIcePixels_percentage":
            item.properties["s3:snowOrIcePixels_percentage"],
            "salineWaterPixels_percentage":
            item.properties["s3:salineWaterPixels_percentage"],
            "coastalPixelss_percentage":
            item.properties["s3:coastalPixelss_percentage"],
            "freshInlandWaterPixels_percentage":
            item.properties["s3:freshInlandWaterPixels_percentage"],
            "tidalRegionPixels_percentage":
            item.properties["s3:tidalRegionPixels_percentage"],
            "landPixels_percentage":
            item.properties["s3:landPixels_percentage"]
        }

        expected = {
            "bbox": [-98.2945, -49.2134, 115.456, 89.5354],
            "datetime": "2021-07-03T14:44:48.463954Z",
            "orbit_state": "ascending",
            "absolute_orbit": 28003,
            "relative_orbit": 310,
            "cloud_cover": 1.692044,
            "instrument": "SYNERGY",
            "mode": "EO",
            "productType": "SY_2_VGP___",
            "snowOrIcePixels_percentage": 0.436467,
            "salineWaterPixels_percentage": 67.744293,
            "coastalPixelss_percentage": 0.169447,
            "freshInlandWaterPixels_percentage": 0.878855,
            "tidalRegionPixels_percentage": 0.470567,
            "landPixels_percentage": 32.227482
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)
