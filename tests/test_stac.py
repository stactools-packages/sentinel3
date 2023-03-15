from pathlib import Path

from stactools.sentinel3 import stac


def test_id(ol_1_efr: Path) -> None:
    item = stac.create_item(str(ol_1_efr), skip_nc=True)
    assert item.id == "S3A_OL_1_EFR_20211021T073827_20211021T074112_0164_077_334_4320"
