import unittest

import pystac
from pystac.extensions.eo import EOExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.sat import SatExtension

from stactools.sentinel3.metadata_links import MetadataLinks
from stactools.sentinel3.product_metadata import ProductMetadata
from stactools.sentinel3.properties import (fill_eo_properties,
                                            fill_proj_properties,
                                            fill_sat_properties)
from tests import test_data


class Sentinel3OLCIMetadataTest(unittest.TestCase):
    def test_parses_olci_1_efr_metadata_properties(self):

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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

    def test_parses_olci_1_err_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3B_OL_1_ERR____20210902T054142_20210902T062554_20210903T103126_"
            "2652_056_262______LN1_O_NT_002.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "bbox": [-179.992, -64.7838, 177.69, 89.2419],
            "epsg": 4326,
            "datetime": "2021-09-02T06:03:47.955487Z",
            "orbit_state": "ascending",
            "absolute_orbit": 17474,
            "relative_orbit": 262,
            "shape": [1217, 15070],
            "instrument": "OLCI",
            "mode": "EO",
            "productType": "OL_1_ERR___",
            "salineWaterPixels_percentage": 64.0,
            "coastalPixels_percentage": 0.0,
            "freshInlandWaterPixels_percentage": 1.0,
            "tidalRegionPixels_percentage": 0.0,
            "brightPixels_percentage": 37.0,
            "invalidPixels_percentage": 3.0,
            "cosmeticPixels_percentage": 0.0,
            "duplicatedPixels_percentage": 0.0,
            "saturatedPixels_percentage": 0.0,
            "dubiousSamples_percentage": 0.0,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_olci_2_lfr_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_OL_2_LFR____20180105T002409_20180105T002540_20180106T053045_"
            "0090_026_216_2069_LN1_O_NT_002.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
        }

        expected = {
            "bbox": [140.405, 50.1222, 162.085, 57.9697],
            "epsg": 4326,
            "datetime": "2018-01-05T00:24:54.153465Z",
            "orbit_state": "descending",
            "absolute_orbit": 9814,
            "relative_orbit": 216,
            "cloud_cover": 71.0,
            "shape": [4865, 2062],
            "instrument": "OLCI",
            "mode": "EO",
            "productType": "OL_2_LFR___",
            "salineWaterPixels_percentage": 13.0,
            "coastalPixels_percentage": 0.002661,
            "freshInlandWaterPixels_percentage": 0.0,
            "tidalRegionPixels_percentage": 1.0,
            "landPixels_percentage": 0.0,
            "invalidPixels_percentage": 4.0,
            "cosmeticPixels_percentage": 0.0,
            "duplicatedPixels_percentage": 0.808174,
            "saturatedPixels_percentage": 0.0,
            "dubiousSamples_percentage": 0.0,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_olci_2_lrr_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3B_OL_2_LRR____20210902T054142_20210902T062554_20210903T103456_"
            "2652_056_262______LN1_O_NT_002.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
        }

        expected = {
            "bbox": [-179.992, -64.7838, 177.69, 89.2419],
            "epsg": 4326,
            "datetime": "2021-09-02T06:03:47.955487Z",
            "orbit_state": "ascending",
            "absolute_orbit": 17474,
            "relative_orbit": 262,
            "cloud_cover": 42.0,
            "shape": [1217, 15070],
            "instrument": "OLCI",
            "mode": "EO",
            "productType": "OL_2_LRR___",
            "salineWaterPixels_percentage": 29.0,
            "coastalPixels_percentage": 0.218855,
            "freshInlandWaterPixels_percentage": 1.0,
            "tidalRegionPixels_percentage": 0.0,
            "landPixels_percentage": 24.0,
            "invalidPixels_percentage": 3.0,
            "cosmeticPixels_percentage": 0.0,
            "duplicatedPixels_percentage": 0.0,
            "saturatedPixels_percentage": 0.0,
            "dubiousSamples_percentage": 0.0,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_olci_2_wfr_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_OL_2_WFR____20201006T012547_20201006T012847_20201007T100122_"
            "0180_063_302_3060_MAR_O_NT_002.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
        }

        expected = {
            "bbox": [117.198, -13.3386, 131.246, -0.122527],
            "epsg": 4326,
            "datetime": "2020-10-06T01:27:17.328426Z",
            "orbit_state": "descending",
            "absolute_orbit": 24145,
            "relative_orbit": 302,
            "cloud_cover": 51.0,
            "shape": [4865, 4091],
            "instrument": "OLCI",
            "mode": "EO",
            "productType": "OL_2_WFR___",
            "salineWaterPixels_percentage": 41.0,
            "coastalPixels_percentage": 0.010557,
            "freshInlandWaterPixels_percentage": 0.0,
            "tidalRegionPixels_percentage": 2.0,
            "landPixels_percentage": 5.0,
            "invalidPixels_percentage": 4.0,
            "cosmeticPixels_percentage": 0.0,
            "duplicatedPixels_percentage": 1.570717,
            "saturatedPixels_percentage": 0.0,
            "dubiousSamples_percentage": 2.0,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_slstr_1_rbt_metadata_properties(self):

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "cloud_cover": 12.909653,
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

    def test_parses_slstr_2_frp_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SL_2_FRP____20201104T001225_20201104T001525_20201105T060455_"
            "0179_064_330_1800_LN2_O_NT_004.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "bbox": [-179.696, 59.3275, 179.51, 73.3617],
            "epsg": 4326,
            "datetime": "2020-11-04T00:13:54.939130Z",
            "orbit_state": "descending",
            "absolute_orbit": 24558,
            "relative_orbit": 330,
            "cloud_cover": 90.616444,
            "shape": [1500, 1200],
            "instrument": "SLSTR",
            "mode": "EO",
            "productType": "SL_2_FRP___",
            "salineWaterPixels_percentage": 16.259833,
            "landPixels_percentage": 83.740167,
            "coastalPixels_percentage": 0.110222,
            "freshInlandWaterPixels_percentage": 2.344778,
            "tidalRegionPixels_percentage": 0.256222,
            "cosmeticPixels_percentage": 22.062722,
            "duplicatedPixels_percentage": 5.217167,
            "saturatedPixels_percentage": 0.0,
            "outOfRangePixels_percentage": 0.182278,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_slstr_2_lst_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SL_2_LST____20180104T004105_20180104T022205_20180930T071122_"
            "6059_026_202______LR1_R_NT_003.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "bbox": [-178.494, -85.7857, 176.014, 89.8585],
            "epsg": 4326,
            "datetime": "2018-01-04T01:31:35.029797Z",
            "orbit_state": "ascending",
            "absolute_orbit": 9800,
            "relative_orbit": 202,
            "cloud_cover": 73.828503,
            "shape": [1500, 40396],
            "instrument": "SLSTR",
            "mode": "EO",
            "productType": "SL_2_LST___",
            "salineWaterPixels_percentage": 63.373017,
            "landPixels_percentage": 36.626983,
            "coastalPixels_percentage": 0.125689,
            "freshInlandWaterPixels_percentage": 0.818881,
            "tidalRegionPixels_percentage": 0.642805,
            "cosmeticPixels_percentage": 23.04911,
            "duplicatedPixels_percentage": 5.590684,
            "saturatedPixels_percentage": 0.0,
            "outOfRangePixels_percentage": 0.0,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_slstr_2_wst_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SL_2_WST____20190505T045344_20190505T063444_20190506T134130_"
            "6059_044_204______MAR_O_NT_003.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            "bbox": [-178.8, -85.9058, 170.226, 89.0387],
            "epsg": 4326,
            "datetime": "2019-05-05T05:44:14.154220Z",
            "orbit_state": "descending",
            "absolute_orbit": 16732,
            "relative_orbit": 204,
            "cloud_cover": 63.849162,
            "shape": [1500, 40396],
            "instrument": "SLSTR",
            "mode": "EO",
            "productType": "SL_2_WST___",
            "salineWaterPixels_percentage": 67.822984,
            "landPixels_percentage": 32.177016,
            "coastalPixels_percentage": 0.0,
            "freshInlandWaterPixels_percentage": 0.0,
            "tidalRegionPixels_percentage": 0.0,
            "cosmeticPixels_percentage": 42.348152,
            "duplicatedPixels_percentage": 0.0,
            "saturatedPixels_percentage": 0.0,
            "outOfRangePixels_percentage": 25.145676,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_sral_2_lan_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SR_2_LAN____20201003T195855_20201003T204924_20201028T210401_"
            "3029_063_270______LN3_O_NT_004.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "bbox": [-72.2571, -81.4165, 120.308, 81.4178],
            "epsg": 4326,
            "datetime": "2020-10-03T20:24:09.317133Z",
            "orbit_state": "ascending",
            "absolute_orbit": 24113,
            "relative_orbit": 270,
            "instrument": "SRAL",
            "mode": "EO",
            "productType": "SR_2_LAN___",
            "lrmModePercentage": 0.0,
            "sarModePercentage": 100.0,
            "landPercentage": 55.0,
            "closedSeaPercentage": 0.0,
            "continentalIcePercentage": 22.0,
            "openOceanPercentage": 23.0,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_sral_2_wat_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SR_2_WAT____20190326T011836_20190326T020243_20190420T170416_"
            "2647_043_017______MAR_O_NT_003.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "bbox": [-172.503, -65.9996, 179.499, 81.4155],
            "epsg": 4326,
            "datetime": "2019-03-26T01:40:39.237989Z",
            "orbit_state": "descending",
            "absolute_orbit": 16160,
            "relative_orbit": 17,
            "instrument": "SRAL",
            "mode": "EO",
            "productType": "SR_2_WAT___",
            "lrmModePercentage": 0.0,
            "sarModePercentage": 100.0,
            "landPercentage": 3.0,
            "closedSeaPercentage": 0.0,
            "continentalIcePercentage": 0.0,
            "openOceanPercentage": 97.0,
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_synergy_2_aod_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SY_2_AOD____20201119T153545_20201119T162000_20201120T223531_"
            "2655_065_168______LN2_O_NT_002.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "cloud_cover":
            item.properties["eo:cloud_cover"],
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
            item.properties["s3:landPixels_percentage"]
        }

        expected = {
            "bbox": [-178.594, -84.4117, 177.852, 61.9656],
            "epsg": 4326,
            "datetime": "2020-11-19T15:57:52.526511Z",
            "orbit_state": "descending",
            "absolute_orbit": 24781,
            "relative_orbit": 168,
            "cloud_cover": 78.520162,
            "shape": [324, 4023],
            "instrument": "SYNERGY",
            "mode": "EO",
            "productType": "SY_2_AOD___",
            "salineWaterPixels_percentage": 73.501939,
            "landPixels_percentage": 26.485775
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_synergy_2_syn_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SY_2_SYN____20190202T004600_20190202T004900_20190203T142947_"
            "0179_041_045_2700_LN2_O_NT_002.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "bbox": [130.373, 7.90436, 144.644, 20.9353],
            "epsg": 4326,
            "datetime": "2019-02-02T00:47:30.461765Z",
            "orbit_state": "descending",
            "absolute_orbit": 15418,
            "relative_orbit": 45,
            "cloud_cover": 39.446131,
            "instrument": "SYNERGY",
            "mode": "EO",
            "productType": "SY_2_SYN___",
            "salineWaterPixels_percentage": 95.649619,
            "coastalPixels_percentage": 0.004361,
            "freshInlandWaterPixels_percentage": 3e-05,
            "tidalRegionPixels_percentage": 0.0,
            "landPixels_percentage": 0.005341
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_synergy_2_v10_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SY_2_V10____20191216T110000_20191226T110000_20200105T114106_"
            "ASIAN_ISLANDS_____LN2_O_NT_002.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            item.datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
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
            "bbox": [92.0045, -11.9955, 169.996, 28.9955],
            "epsg": 4326,
            "datetime": "2019-12-21T11:00:00Z",
            "orbit_state": "descending",
            "absolute_orbit": 19931,
            "relative_orbit": 323,
            "cloud_cover": 4.358878,
            "instrument": "SYNERGY",
            "mode": "EO",
            "productType": "SY_2_V10___",
            "snowOrIcePixels_percentage": 0.027358,
            "landPixels_percentage": 18.263485
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_synergy_2_vg1_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3A_SY_2_VG1____20200609T120000_20200610T120000_20200615T121610_"
            "CENTRAL_AMERICA___LN2_O_NT_002.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            item.datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
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
            "bbox": [-124.991, 3.60956e-12, -50.0, 49.9911],
            "epsg": 4326,
            "datetime": "2020-06-10T00:00:00Z",
            "orbit_state": "ascending",
            "absolute_orbit": 22455,
            "relative_orbit": 152,
            "cloud_cover": 9.465587,
            "instrument": "SYNERGY",
            "mode": "EO",
            "productType": "SY_2_VG1___",
            "snowOrIcePixels_percentage": 0.066818,
            "landPixels_percentage": 22.527562
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)

    def test_parses_synergy_2_vgp_metadata_properties(self):

        # Get the path of the test xml
        manifest_path = test_data.get_path(
            "data-files/"
            "S3B_SY_2_VGP____20210213T192726_20210213T201112_20210215T060438_"
            "2626_049_099______LN2_O_NT_002.SEN3")

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

        # eo
        eo = EOExtension.ext(item, add_if_missing=True)
        fill_eo_properties(eo, metalinks.product_metadata_href)

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
            "bbox": [-179.336, -84.0126, 179.986, 68.7507],
            "epsg": 4326,
            "datetime": "2021-02-13T19:49:19.044416Z",
            "orbit_state": "descending",
            "absolute_orbit": 14616,
            "relative_orbit": 99,
            "cloud_cover": 0.280665,
            "instrument": "SYNERGY",
            "mode": "EO",
            "productType": "SY_2_VGP___",
            "snowOrIcePixels_percentage": 0.207021,
            "salineWaterPixels_percentage": 86.89342,
            "coastalPixelss_percentage": 0.048629,
            "freshInlandWaterPixels_percentage": 0.355955,
            "tidalRegionPixels_percentage": 0.062851,
            "landPixels_percentage": 13.090312
        }

        for k, v in expected.items():
            self.assertIn(k, s3_props)
            self.assertEqual(s3_props[k], v)
