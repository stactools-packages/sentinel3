from pystac.extensions.sat import OrbitState
from stactools.core.io.xml import XmlElement


def fill_sat_properties(sat_ext, href):
    """Fills the properties for SAR.

    Based on the sat Extension.py

    Args:
        sat_ext (pystac.extensions.sat.SatExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an XML file.

    Returns:
        pystac.Asset: An asset with the SAT relevant properties.
    """
    # Read meta file
    root = XmlElement.from_file(href)

    sat_ext.platform_international_designator = root.findall(
        ".//sentinel-safe:nssdcIdentifier")[0].text

    orbit_state = root.find_attr("groundTrackDirection",
                                 ".//sentinel-safe:orbitNumber")
    sat_ext.orbit_state = OrbitState(orbit_state)

    sat_ext.absolute_orbit = int(
        root.findall(".//sentinel-safe:orbitNumber")[0].text)

    sat_ext.relative_orbit = int(
        root.findall(".//sentinel-safe:relativeOrbitNumber")[0].text)


def fill_eo_properties(eo_ext, href):
    """Fills the properties for EO.

    Based on the eo Extension.py

    Args:
        eo_ext (pystac.extensions.eo.EOExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an XML file.

    Returns:
        pystac.Asset: An asset with the EO relevant properties.
    """
    # Read meta file
    root = XmlElement.from_file(href)
    product_name = root.findall(".//sentinel3:productName")[0].text
    if product_name.split("_")[1] == "OL" and product_name.split(
            "_")[2] == "1":
        pass
    elif product_name.split("_")[1] == "OL" and product_name.split(
            "_")[2] == "2":
        eo_ext.cloud_cover = float(
            root.find_attr("percentage", ".//sentinel3:cloudyPixels"))
    elif product_name.split("_")[1] == "SL":
        eo_ext.cloud_cover = float(
            root.find_attr("percentage", ".//sentinel3:cloudyPixels"))
    else:
        raise ValueError("Unexpected value found at "
                         f"{product_name}: "
                         "this was expected to follow the sentinel 3 "
                         "naming convention, including "
                         "ending in .SEN3")


def fill_proj_properties(proj_ext, product_meta):
    """Fills the properties for PROJ.

    Based on the proj Extension.py

    Args:
        proj_ext (pystac.extensions.projection.ProjectionExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an XML file.

    Returns:
        pystac.Asset: An asset with the PROJECTION relevant properties.
    """
    # Read meta file

    proj_ext.epsg = product_meta.get_epsg

    proj_ext.shape = product_meta.get_shape
