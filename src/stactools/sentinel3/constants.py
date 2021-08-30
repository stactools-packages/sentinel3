import pystac
from pystac import ProviderRole
from pystac.link import Link
from pystac.extensions.eo import Band

INSPIRE_METADATA_ASSET_KEY = "inspire-metadata"
SAFE_MANIFEST_ASSET_KEY = "safe-manifest"
PRODUCT_METADATA_ASSET_KEY = "product-metadata"

SENTINEL_LICENSE = Link(
    rel="license",
    target="https://sentinel.esa.int/documents/" +
    "247904/690755/Sentinel_Data_Legal_Notice",
)

SENTINEL_CONSTELLATION = "Sentinel 3"

SENTINEL_INSTRUMENTS = ['slstr']

SENTINEL_PROVIDER = pystac.Provider(
    name="ESA",
    roles=[
        ProviderRole.PRODUCER,
        ProviderRole.PROCESSOR,
        ProviderRole.LICENSOR,
    ],
    url="https://earth.esa.int/web/guest/home",
)

SAFE_MANIFEST_ASSET_KEY = "safe-manifest"

SENTINEL_LICENSE = Link(
    rel="license",
    target="https://sentinel.esa.int/documents/" +
    "247904/690755/Sentinel_Data_Legal_Notice",
)

X_SIZE = 10000
Y_SIZE = 10000
