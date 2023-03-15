import shutil
from pathlib import Path

from stactools.sentinel3 import stac

root = Path(__file__).parents[1]
examples = root / "examples"
data_files = root / "tests" / "data-files"

if examples.exists():
    shutil.rmtree(examples)

examples.mkdir()

for path in data_files.glob("*.SEN3"):
    item = stac.create_item(str(path), skip_nc=False)
    item.set_self_href(str(examples / item.id) + ".json")
    item.make_asset_hrefs_relative()
    item.save_object(include_self_link=False)
