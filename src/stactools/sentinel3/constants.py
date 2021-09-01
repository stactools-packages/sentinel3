import pystac
from pystac import ProviderRole
from pystac.extensions.eo import Band
from pystac.link import Link

INSPIRE_METADATA_ASSET_KEY = "inspire-metadata"
SAFE_MANIFEST_ASSET_KEY = "safe-manifest"
PRODUCT_METADATA_ASSET_KEY = "product-metadata"

SENTINEL_LICENSE = Link(
    rel="license",
    target="https://sentinel.esa.int/documents/" +
    "247904/690755/Sentinel_Data_Legal_Notice",
)

SENTINEL_CONSTELLATION = "Sentinel 3"

SENTINEL_INSTRUMENTS = ["slstr"]

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
    "S01":
    Band.create(
        name="S1",
        description="Band 1 - Cloud screening, vegetation monitoring, aerosol",
        center_wavelength=554.27,
        full_width_half_max=19.26,
    ),
    "S02":
    Band.create(
        name="S2",
        description="Band 2 - NDVI, vegetation monitoring, aerosol",
        center_wavelength=659.47,
        full_width_half_max=19.25,
    ),
    "S03":
    Band.create(
        name="S3",
        description="Band 3 - NDVI, cloud flagging, pixel co-registration",
        center_wavelength=868,
        full_width_half_max=20.6,
    ),
    "S04":
    Band.create(
        name="S4",
        description="Band 4 - Cirrus detection over land",
        center_wavelength=1374.8,
        full_width_half_max=20.8,
    ),
    "S05":
    Band.create(
        name="S5",
        description="Band 5 - Cloud clearing, ice, snow, vegetation monitoring",
        center_wavelength=1613.4,
        full_width_half_max=60.68,
    ),
    "S06":
    Band.create(
        name="S6",
        description="Band 6 - Vegetation state and cloud clearing",
        center_wavelength=2255.7,
        full_width_half_max=50.15,
    ),
    "S07":
    Band.create(
        name="S7",
        description="Band 7 - SST, LST, Active fire",
        center_wavelength=3742,
        full_width_half_max=398,
    ),
    "S08":
    Band.create(
        name="S8",
        description="Band 8 - SST, LST, Active fire",
        center_wavelength=10854,
        full_width_half_max=776,
    ),
    "S09":
    Band.create(
        name="S9",
        description="Band 9 - SST, LST",
        center_wavelength=12022.5,
        full_width_half_max=905,
    ),
    "S10":
    Band.create(
        name="F1",
        description="Band 10 - Active fire",
        center_wavelength=3742,
        full_width_half_max=398,
    ),
    "S11":
    Band.create(
        name="F2",
        description="Band 11 - Active fire",
        center_wavelength=10854,
        full_width_half_max=776,
    ),
}

SENTINEL_OLCI_BANDS = {
    "Oa01":
    Band.create(
        name="Oa01",
        description="Band 1 - Aerosol correction, "
        "improved water constituent retrieval",
        center_wavelength=400,
        full_width_half_max=15,
    ),
    "Oa02":
    Band.create(
        name="Oa02",
        description="Band 2 - Yellow substance "
        "and detrital pigments (turbidity)",
        center_wavelength=412.5,
        full_width_half_max=10,
    ),
    "Oa03":
    Band.create(
        name="Oa03",
        description="Band 3 - Chlorophyll absorption "
        "maximum, biogeochemistry, vegetation",
        center_wavelength=442.5,
        full_width_half_max=10,
    ),
    "Oa04":
    Band.create(
        name="Oa04",
        description="Band 4 - Chlorophyll",
        center_wavelength=490,
        full_width_half_max=10,
    ),
    "Oa05":
    Band.create(
        name="Oa05",
        description="Band 5 - Chlorophyll, sediment, turbidity, red tide",
        center_wavelength=510,
        full_width_half_max=10,
    ),
    "Oa06":
    Band.create(
        name="Oa06",
        description="Band 6 - Chlorophyll reference (minimum)",
        center_wavelength=560,
        full_width_half_max=10,
    ),
    "Oa07":
    Band.create(
        name="Oa07",
        description="Band 7 - Sediment loading",
        center_wavelength=620,
        full_width_half_max=10,
    ),
    "Oa08":
    Band.create(
        name="Oa08",
        description="Band 8 - 2nd Chlorophyll absorption "
        "maximum, sediment, yellow substance / vegetation",
        center_wavelength=665,
        full_width_half_max=10,
    ),
    "Oa09":
    Band.create(
        name="Oa09",
        description="Band 9 - Improved fluorescence retrieval",
        center_wavelength=673.75,
        full_width_half_max=7.5,
    ),
    "Oa10":
    Band.create(
        name="Oa10",
        description="Band 10 - Chlorophyll fluorescence peak, red edge",
        center_wavelength=681.25,
        full_width_half_max=7.5,
    ),
    "Oa11":
    Band.create(
        name="Oa11",
        description="Band 11 - Chlorophyll fluorescence "
        "baseline, red edge transition",
        center_wavelength=708.75,
        full_width_half_max=10,
    ),
    "Oa12":
    Band.create(
        name="Oa12",
        description="Band 12 - O2 absorption / clouds, vegetation",
        center_wavelength=753.75,
        full_width_half_max=7.5,
    ),
    "Oa13":
    Band.create(
        name="Oa13",
        description="Band 13 - O2 absorption / aerosol correction",
        center_wavelength=761.25,
        full_width_half_max=2.5,
    ),
    "Oa14":
    Band.create(
        name="Oa14",
        description="Band 14 - Atmospheric correction",
        center_wavelength=764.375,
        full_width_half_max=3.75,
    ),
    "Oa15":
    Band.create(
        name="Oa15",
        description="Band 15 - O2 absorption used for "
        "cloud top pressure, fluorescence over land",
        center_wavelength=767.5,
        full_width_half_max=2.5,
    ),
    "Oa16":
    Band.create(
        name="Oa16",
        description="Band 16 - Atmospheric / aerosol correction",
        center_wavelength=778.75,
        full_width_half_max=15,
    ),
    "Oa17":
    Band.create(
        name="Oa17",
        description="Band 17 - Atmospheric / aerosol "
        "correction, clouds, pixel co-registration",
        center_wavelength=865,
        full_width_half_max=20,
    ),
    "Oa18":
    Band.create(
        name="Oa18",
        description="Band 18 - Water vapour absorption reference. "
        "Common reference band with SLSTR. Vegetation monitoring",
        center_wavelength=885,
        full_width_half_max=10,
    ),
    "Oa19":
    Band.create(
        name="Oa19",
        description="Band 19 - Water vapour absorption, "
        "vegetation monitoring (maximum REFLECTANCE)",
        center_wavelength=900,
        full_width_half_max=10,
    ),
    "Oa20":
    Band.create(
        name="Oa20",
        description="Band 20 - Water vapour absorption, "
        "atmospheric / aerosol correction",
        center_wavelength=940,
        full_width_half_max=20,
    ),
    "Oa21":
    Band.create(
        name="Oa21",
        description="Band 21 - Water vapour absorption, "
        "atmospheric / aerosol correction",
        center_wavelength=1020,
        full_width_half_max=40,
    ),
}

OLCI_BANDS_TO_RESOLUTIONS = {
    "Oa01": [
        300,
    ],
    "Oa02": [
        300,
    ],
    "Oa03": [
        300,
    ],
    "Oa04": [
        300,
    ],
    "Oa05": [
        300,
    ],
    "Oa06": [
        300,
    ],
    "Oa07": [
        300,
    ],
    "Oa08": [
        300,
    ],
    "Oa09": [
        300,
    ],
    "Oa10": [
        300,
    ],
    "Oa11": [
        300,
    ],
    "Oa12": [
        300,
    ],
    "Oa13": [
        300,
    ],
    "Oa14": [
        300,
    ],
    "Oa15": [
        300,
    ],
    "Oa16": [
        300,
    ],
    "Oa17": [
        300,
    ],
    "Oa18": [
        300,
    ],
    "Oa19": [
        300,
    ],
    "Oa20": [
        300,
    ],
    "Oa21": [
        300,
    ],
}

SLSTR_BANDS_TO_RESOLUTIONS = {
    "S01": [
        500,
    ],
    "S02": [
        500,
    ],
    "S03": [
        500,
    ],
    "S04": [
        500,
    ],
    "S05": [
        500,
    ],
    "S06": [
        500,
    ],
    "S07": [
        1000,
    ],
    "S08": [
        1000,
    ],
    "S09": [
        1000,
    ],
    "S10": [
        1000,
    ],
    "S11": [
        1000,
    ],
}

SENTINEL_LICENSE = Link(
    rel="license",
    target="https://sentinel.esa.int/documents/" +
    "247904/690755/Sentinel_Data_Legal_Notice",
)
