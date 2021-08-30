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

SENTINEL_SLSTR_BANDS = {
    'S01':
    Band.create(name='S1',
                description='Band 1 - Cloud screening, vegetation monitoring, aerosol',
                center_wavelength=554.27,
                bandwidth=19.26),
    'S02':
    Band.create(name='S2',
                description='Band 2 - NDVI, vegetation monitoring, aerosol',
                center_wavelength=659.47,
                bandwidth=19.25),
    'S03':
    Band.create(name='S3',
                description='Band 3 - NDVI, cloud flagging, pixel co-registration',
                center_wavelength=868,
                bandwidth=20.6),
    'S04':
    Band.create(name='S4',
                description='Band 4 - Cirrus detection over land',
                center_wavelength=1374.8,
                bandwidth=20.8),
    'S05':
    Band.create(name='S5',
                description='Band 5 - Cloud clearing, ice, snow, vegetation monitoring',
                center_wavelength=1613.4,
                bandwidth=60.68),
    'S06':
    Band.create(name='S6',
                description='Band 6 - Vegetation state and cloud clearing',
                center_wavelength=2255.7,
                bandwidth=50.15),    
    'S07':
    Band.create(name='S7',
                description='Band 7 - SST, LST, Active fire',
                center_wavelength=3742,
                bandwidth=398),
    'S08':
    Band.create(name='S8',
                description='Band 8 - SST, LST, Active fire',
                center_wavelength=10854,
                bandwidth=776),
    'S09':
    Band.create(name='S9',
                description='Band 9 - SST, LST',
                center_wavelength=12022.5,
                bandwidth=905),
    'S10':
    Band.create(name='F1',
                description='Band 10 - Active fire',
                center_wavelength=3742,
                bandwidth=398),
    'S11':
    Band.create(name='F2',
                description='Band 11 - Active fire',
                center_wavelength=10854,
                bandwidth=776),    
}

SENTINEL_LICENSE = Link(
    rel="license",
    target="https://sentinel.esa.int/documents/" +
    "247904/690755/Sentinel_Data_Legal_Notice",
)

X_SIZE = 10000
Y_SIZE = 10000
