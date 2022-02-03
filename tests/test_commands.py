import os
from tempfile import TemporaryDirectory

import pystac
from pystac.extensions.eo import EOExtension
from pystac.utils import is_absolute_href
from stactools.testing import CliTestCase

from stactools.sentinel3.commands import create_sentinel3_command
from stactools.sentinel3.constants import (SENTINEL_OLCI_BANDS,
                                           SENTINEL_SLSTR_BANDS,
                                           SENTINEL_SRAL_BANDS,
                                           SENTINEL_SYNERGY_BANDS)
from tests import test_data


class CreateItemTest(CliTestCase):

    def create_subcommand_functions(self):
        return [create_sentinel3_command]

    def test_create_olci_1_efr_item(self):
        item_id = str("S3A_OL_1_EFR____"
                      "20211021T073827_20211021T074112_20211021T091357_"
                      "0164_077_334_4320_LN1_O_NR_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_OL_1_EFR____"
            "20211021T073827_20211021T074112_20211021T091357_"
            "0164_077_334_4320_LN1_O_NR_002.SEN3")

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
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_olci_1_err_item(self):
        item_id = str("S3B_OL_1_ERR____"
                      "20210831T200148_20210831T204600_20210902T011514_"
                      "2652_056_242______LN1_O_NT_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3B_OL_1_ERR____"
            "20210831T200148_20210831T204600_20210902T011514_"
            "2652_056_242______LN1_O_NT_002.SEN3")

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
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_olci_2_lfr_item(self):
        item_id = str("S3A_OL_2_LFR____"
                      "20210523T003029_20210523T003329_20210524T050403_"
                      "0179_072_102_1980_LN1_O_NT_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_OL_2_LFR____"
            "20210523T003029_20210523T003329_20210524T050403_"
            "0179_072_102_1980_LN1_O_NT_002.SEN3")

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
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_olci_2_lrr_item(self):
        item_id = str("S3B_OL_2_LRR____"
                      "20210731T214325_20210731T222741_20210802T020007_"
                      "2656_055_186______LN1_O_NT_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3B_OL_2_LRR____"
            "20210731T214325_20210731T222741_20210802T020007_"
            "2656_055_186______LN1_O_NT_002.SEN3")

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
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_olci_2_wfr_item(self):
        item_id = str("S3A_OL_2_WFR____"
                      "20210604T001016_20210604T001316_20210604T021918_"
                      "0179_072_273_1440_MAR_O_NR_003")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_OL_2_WFR____"
            "20210604T001016_20210604T001316_20210604T021918_"
            "0179_072_273_1440_MAR_O_NR_003.SEN3")

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
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_slstr_1_rbt_item(self):
        item_id = str("S3A_SL_1_RBT____"
                      "20210930T220914_20210930T221214_20211002T102150_"
                      "0180_077_043_5400_LN2_O_NT_004")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SL_1_RBT____"
            "20210930T220914_20210930T221214_20211002T102150_"
            "0180_077_043_5400_LN2_O_NT_004.SEN3")

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
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_slstr_2_frp_item(self):
        item_id = str("S3A_SL_2_FRP____"
                      "20210802T000420_20210802T000720_20210803T123912_"
                      "0179_074_344_2880_LN2_O_NT_004")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SL_2_FRP____"
            "20210802T000420_20210802T000720_20210803T123912_"
            "0179_074_344_2880_LN2_O_NT_004.SEN3")

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
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_slstr_2_lst_item(self):
        item_id = str("S3A_SL_2_LST____"
                      "20210510T002955_20210510T003255_20210511T101010_"
                      "0179_071_301_5760_LN2_O_NT_004")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SL_2_LST____"
            "20210510T002955_20210510T003255_20210511T101010_"
            "0179_071_301_5760_LN2_O_NT_004.SEN3")

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
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_slstr_2_wst_item(self):
        item_id = str("S3B_SL_2_WST____"
                      "20210419T051754_20210419T065853_20210420T160434_"
                      "6059_051_247______MAR_O_NT_003")
        granule_href = test_data.get_path(
            "data-files/"
            "S3B_SL_2_WST____"
            "20210419T051754_20210419T065853_20210420T160434_"
            "6059_051_247______MAR_O_NT_003.SEN3")

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
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_sral_2_lan_item(self):
        item_id = str("S3A_SR_2_LAN____"
                      "20210611T011438_20210611T012436_20210611T024819_"
                      "0598_072_373______LN3_O_NR_004")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SR_2_LAN____"
            "20210611T011438_20210611T012436_20210611T024819_"
            "0598_072_373______LN3_O_NR_004.SEN3")

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
                    value.name for value in SENTINEL_SRAL_BANDS.values()
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_sral_2_wat_item(self):
        item_id = str("S3A_SR_2_WAT____"
                      "20210704T012815_20210704T021455_20210729T173140_"
                      "2800_073_316______MAR_O_NT_004")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SR_2_WAT____"
            "20210704T012815_20210704T021455_20210729T173140_"
            "2800_073_316______MAR_O_NT_004.SEN3")

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
                    value.name for value in SENTINEL_SRAL_BANDS.values()
                ]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_synergy_2_aod_item(self):
        item_id = str("S3B_SY_2_AOD____"
                      "20210512T143315_20210512T151738_20210514T064157_"
                      "2663_052_196______LN2_O_NT_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3B_SY_2_AOD____"
            "20210512T143315_20210512T151738_20210514T064157_"
            "2663_052_196______LN2_O_NT_002.SEN3")

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
                    value.name for value in SENTINEL_SYNERGY_BANDS.values()
                ][26:32]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_synergy_2_syn_item(self):
        item_id = str("S3A_SY_2_SYN____"
                      "20210325T005418_20210325T005718_20210325T142858_"
                      "0180_070_031_1620_LN2_O_ST_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SY_2_SYN____"
            "20210325T005418_20210325T005718_20210325T142858_"
            "0180_070_031_1620_LN2_O_ST_002.SEN3")

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

                combined_bands = {
                    **SENTINEL_OLCI_BANDS,
                    **SENTINEL_SLSTR_BANDS,
                    **SENTINEL_SYNERGY_BANDS
                }

                band_list = [value.name for value in combined_bands.values()]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_synergy_2_v10_item(self):
        item_id = str("S3A_SY_2_V10____"
                      "20210911T000000_20210920T235959_20210928T121452_"
                      "EUROPE____________LN2_O_NT_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SY_2_V10____"
            "20210911T000000_20210920T235959_20210928T121452_"
            "EUROPE____________LN2_O_NT_002.SEN3")

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
                    value.name for value in SENTINEL_SYNERGY_BANDS.values()
                ][-4:]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_synergy_2_vg1_item(self):
        item_id = str("S3A_SY_2_VG1____"
                      "20211013T000000_20211013T235959_20211014T203456_"
                      "EUROPE____________LN2_O_ST_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SY_2_VG1____"
            "20211013T000000_20211013T235959_20211014T203456_"
            "EUROPE____________LN2_O_ST_002.SEN3")

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
                    value.name for value in SENTINEL_SYNERGY_BANDS.values()
                ][-4:]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")

    def test_create_synergy_2_vgp_item(self):
        item_id = str("S3A_SY_2_VGP____"
                      "20210703T142237_20210703T150700_20210703T211742_"
                      "2663_073_310______LN2_O_ST_002")
        granule_href = test_data.get_path(
            "data-files/"
            "S3A_SY_2_VGP____"
            "20210703T142237_20210703T150700_20210703T211742_"
            "2663_073_310______LN2_O_ST_002.SEN3")

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
                    value.name for value in SENTINEL_SYNERGY_BANDS.values()
                ][-4:]

                bands_seen = set()

                for _, asset in item.assets.items():
                    self.assertTrue("/./" not in asset.href)
                    self.assertTrue(is_absolute_href(asset.href))
                    asset_eo = EOExtension.ext(asset)
                    bands = asset_eo.bands
                    if bands is not None:
                        bands_seen |= set(b.name for b in bands)

                [self.assertTrue(band in band_list) for band in bands_seen]
                os.remove(f"{tmp_dir}/{item_id}.json")
