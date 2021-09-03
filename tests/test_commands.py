import os
from tempfile import TemporaryDirectory

import pystac
from pystac.utils import is_absolute_href
from stactools.testing import CliTestCase

from stactools.sentinel3.commands import create_sentinel3_command
from stactools.sentinel3.constants import (SENTINEL_OLCI_BANDS,
                                           SENTINEL_SLSTR_BANDS)
from tests import test_data


class CreateItemTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_sentinel3_command]

    def test_create_olci_1_efr_item(self):
        item_id = str("S3A_OL_1_EFR____"
                      "20210820T103153_20210820T103453_20210820T124206_"
                      "0179_075_222_2160_LN1_O_NR_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_OL_1_EFR____"
            "20210820T103153_20210820T103453_20210820T124206_"
            "0179_075_222_2160_LN1_O_NR_002.SEN3")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel3", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    value.name for value in SENTINEL_OLCI_BANDS.values()
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b['name']
                            for b in asset.extra_fields['band_fields'])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_olci_1_err_item(self):
        item_id = str("S3B_OL_1_ERR____"
                      "20210902T054142_20210902T062554_20210903T103126_"
                      "2652_056_262______LN1_O_NT_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3B_OL_1_ERR____"
            "20210902T054142_20210902T062554_20210903T103126_"
            "2652_056_262______LN1_O_NT_002.SEN3")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel3", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    value.name for value in SENTINEL_OLCI_BANDS.values()
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b['name']
                            for b in asset.extra_fields['band_fields'])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_olci_2_lfr_item(self):
        item_id = str("S3A_OL_2_LFR____"
                      "20180105T002409_20180105T002540_20180106T053045_"
                      "0090_026_216_2069_LN1_O_NT_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_OL_2_LFR____"
            "20180105T002409_20180105T002540_20180106T053045_"
            "0090_026_216_2069_LN1_O_NT_002.SEN3")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel3", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    value.name for value in SENTINEL_OLCI_BANDS.values()
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b['name']
                            for b in asset.extra_fields['band_fields'])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_olci_2_lrr_item(self):
        item_id = str("S3B_OL_2_LRR____"
                      "20210902T054142_20210902T062554_20210903T103456_"
                      "2652_056_262______LN1_O_NT_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3B_OL_2_LRR____"
            "20210902T054142_20210902T062554_20210903T103456_"
            "2652_056_262______LN1_O_NT_002.SEN3")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel3", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    value.name for value in SENTINEL_OLCI_BANDS.values()
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b['name']
                            for b in asset.extra_fields['band_fields'])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_olci_2_wfr_item(self):
        item_id = str("S3A_OL_2_WFR____"
                      "20201006T012547_20201006T012847_20201007T100122_"
                      "0180_063_302_3060_MAR_O_NT_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_OL_2_WFR____"
            "20201006T012547_20201006T012847_20201007T100122_"
            "0180_063_302_3060_MAR_O_NT_002.SEN3")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel3", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    value.name for value in SENTINEL_OLCI_BANDS.values()
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b['name']
                            for b in asset.extra_fields['band_fields'])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_slstr_1_rbt_item(self):
        item_id = str("S3A_SL_1_RBT____"
                      "20210827T074336_20210827T074636_20210827T094954_"
                      "0179_075_320_3060_LN2_O_NR_004")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SL_1_RBT____"
            "20210827T074336_20210827T074636_20210827T094954_"
            "0179_075_320_3060_LN2_O_NR_004.SEN3")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel3", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    value.name for value in SENTINEL_SLSTR_BANDS.values()
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b['name']
                            for b in asset.extra_fields['band_fields'])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_slstr_2_frp_item(self):
        item_id = str("S3A_SL_2_FRP____"
                      "20201104T001225_20201104T001525_20201105T060455_"
                      "0179_064_330_1800_LN2_O_NT_004")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SL_2_FRP____"
            "20201104T001225_20201104T001525_20201105T060455_"
            "0179_064_330_1800_LN2_O_NT_004.SEN3")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel3", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    value.name for value in SENTINEL_SLSTR_BANDS.values()
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b['name']
                            for b in asset.extra_fields['band_fields'])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_slstr_2_lst_item(self):
        item_id = str("S3A_SL_2_LST____"
                      "20180104T004105_20180104T022205_20180930T071122_"
                      "6059_026_202______LR1_R_NT_003")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SL_2_LST____"
            "20180104T004105_20180104T022205_20180930T071122_"
            "6059_026_202______LR1_R_NT_003.SEN3")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel3", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    value.name for value in SENTINEL_SLSTR_BANDS.values()
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b['name']
                            for b in asset.extra_fields['band_fields'])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_slstr_2_wst_item(self):
        item_id = str("S3A_SL_2_WST____"
                      "20190505T045344_20190505T063444_20190506T134130_"
                      "6059_044_204______MAR_O_NT_003")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SL_2_WST____"
            "20190505T045344_20190505T063444_20190506T134130_"
            "6059_044_204______MAR_O_NT_003.SEN3")

        with self.subTest(granule_href):
            with TemporaryDirectory() as tmp_dir:
                cmd = ["sentinel3", "create-item", granule_href, tmp_dir]
                self.run_command(cmd)

                jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                self.assertEqual(len(jsons), 1)
                fname = jsons[0]

                item = pystac.Item.from_file(os.path.join(tmp_dir, fname))

                item.validate()

                self.assertEqual(item.id, item_id)

                band_list = [
                    value.name for value in SENTINEL_SLSTR_BANDS.values()
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    if _ == "eo:bands":
                        bands_seen |= set(
                            b['name']
                            for b in asset.extra_fields['band_fields'])
                    else:
                        pass

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")
