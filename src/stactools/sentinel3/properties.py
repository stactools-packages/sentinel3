from pystac.extensions.eo import EOExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.sat import OrbitState, SatExtension
from stactools.core.io.xml import XmlElement

from stactools.sentinel3.product_metadata import ProductMetadata


def fill_sat_properties(sat_ext: SatExtension, manifest: XmlElement):
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


def fill_eo_properties(eo_ext: EOExtension, manifest: XmlElement):
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


def fill_proj_properties(proj_ext: ProjectionExtension,
                         product_meta: ProductMetadata):
    """Fills the properties for PROJ.

    Based on the proj Extension.py

    Args:
        proj_ext (ProjectionExtension): The extension to be populated.
        product_meta (ProductMetadata): An object containing general product metadata.
    """
    # Read meta file

    proj_ext.epsg = product_meta.get_epsg

    if (product_meta.scene_id.split("_")[1] == "SR"
            and product_meta.scene_id.split("_")[2] == "2"):
        pass
    elif (product_meta.scene_id.split("_")[1] == "SY"
          and product_meta.scene_id.split("_")[2] == "2"
          and product_meta.scene_id.split("_")[3] != "AOD"):
        pass
    else:
        proj_ext.shape = product_meta.get_shape
