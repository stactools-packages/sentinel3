from pystac.extensions.eo import EOExtension
from pystac.extensions.sat import OrbitState, SatExtension
from stactools.core.io.xml import XmlElement

from stactools.sentinel3.file_extension_updated import FileExtensionUpdated


def fill_sat_properties(sat_ext: SatExtension, manifest: XmlElement) -> None:
    """Fills the properties for SAR.

    Based on the sat Extension.py

    Args:
        sat_ext (SatExtension): The extension to be populated.
        manifest(XmlElement): manifest file parsed to XmlElement.
    """

    sat_ext.platform_international_designator = manifest.findall(
        ".//sentinel-safe:nssdcIdentifier")[0].text

    orbit_state = manifest.find_attr("groundTrackDirection",
                                     ".//sentinel-safe:orbitNumber")
    sat_ext.orbit_state = OrbitState(orbit_state)

    sat_ext.absolute_orbit = int(
        manifest.findall(".//sentinel-safe:orbitNumber")[0].text)

    relative_orbit_num = int(
        manifest.findall(".//sentinel-safe:relativeOrbitNumber")[0].text)

    if relative_orbit_num == 0:
        sat_ext.relative_orbit = int(
            manifest.findall(
                ".//sentinel-safe:relativeOrbitNumber[@type='stop']")[0].text)
    else:
        sat_ext.relative_orbit = relative_orbit_num


def fill_eo_properties(eo_ext: EOExtension, manifest: XmlElement) -> None:
    """Fills the properties for EO.

    Based on the eo Extension.py

    Args:
        eo_ext (EOExtension): The extension to be populated.
        manifest(XmlElement): manifest file parsed to XmlElement.
    """
    def find_or_throw(attribute: str, xpath: str) -> str:
        value = manifest.find_attr(attribute, xpath)
        if value is None:
            raise RuntimeError(
                f"Value not found in manifest: {xpath}@{attribute}")
        return value

    product_name = manifest.findall(".//sentinel3:productName")[0].text
    if product_name.split("_")[1] == "OL" and product_name.split(
            "_")[2] == "1":
        pass
    elif product_name.split("_")[1] == "OL" and product_name.split(
            "_")[2] == "2":
        eo_ext.cloud_cover = float(
            find_or_throw("percentage", ".//sentinel3:cloudyPixels"))
    elif product_name.split("_")[1] == "SL":
        eo_ext.cloud_cover = float(
            find_or_throw("percentage", ".//sentinel3:cloudyPixels"))
    elif product_name.split("_")[1] == "SR" and product_name.split(
            "_")[2] == "2":
        pass
    elif product_name.split("_")[1] == "SY" and product_name.split(
            "_")[2] == "2":
        eo_ext.cloud_cover = float(
            find_or_throw("percentage", ".//sentinel3:cloudyPixels"))
    else:
        raise ValueError("Unexpected value found at "
                         f"{product_name}: "
                         "this was expected to follow the sentinel 3 "
                         "naming convention, including "
                         "ending in .SEN3")


def fill_file_properties(granule_href: str, asset_key: str,
                         file_ext: FileExtensionUpdated,
                         manifest: XmlElement) -> None:

    file_ext.checksum = manifest.findall(
        f".//dataObject[@ID='{asset_key}']//checksum")[0].text
    manifest_file_location = str(
        manifest.find_attr("href",
                           f".//dataObject[@ID='{asset_key}']//fileLocation"))
    file_ext.local_path = "".join([
        granule_href.split("/")[-1], "/",
        manifest_file_location.replace("./", "")
    ])
    asset_size = manifest.find_attr(
        "size", f".//dataObject[@ID='{asset_key}']//byteStream")

    if file_ext.checksum is None:
        raise RuntimeError(f"Manifest contains no checksum! Checked location: "
                           f"'.//dataObject[@ID='{asset_key}']//checksum'")
    if file_ext.local_path is None:
        raise RuntimeError(
            f"Manifest contains no file location data! Checked location: "
            f"'.//dataObject[@ID='{asset_key}']//fileLocation'")
    if asset_size is None:
        raise RuntimeError(
            f"Manifest contains no size data! Checked location: "
            f"'.//dataObject[@ID='{asset_key}']//byteStream'")

    file_ext.size = int(asset_size)
