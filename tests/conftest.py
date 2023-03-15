from pathlib import Path

import pytest


@pytest.fixture
def ol_1_efr() -> Path:
    return (
        Path(__file__).parent
        / "data-files"
        / (
            "S3A_OL_1_EFR____20211021T073827_20211021T074112_"
            "20211021T091357_0164_077_334_4320_LN1_O_NR_002.SEN3"
        )
    )
