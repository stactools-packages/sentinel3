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
