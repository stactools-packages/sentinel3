from stactools.core.io.xml import XmlElement
from pystac.extensions.sat import OrbitState
from .constants import X_SIZE, Y_SIZE

def fill_sat_properties(sat_ext, href):
    """Fills the properties for SAR.

    Based on the sar Extension.py

    Args:
        input_ext (pystac.extensions.sar.SarExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an XML file.

    Returns:
        pystac.Asset: An asset with the SAR relevant properties.
    """
    # Read meta file
    root = XmlElement.from_file(href)

    sat_ext.platform_international_designator = root.findall(
        ".//sentinel-safe:nssdcIdentifier"
    )[0].text

    orbit_state = root.find_attr(
        "groundTrackDirection", ".//sentinel-safe:orbitNumber"
    )
    sat_ext.orbit_state = OrbitState(orbit_state)

    sat_ext.absolute_orbit = int(root.findall(".//sentinel-safe:orbitNumber")[0].text)

    sat_ext.relative_orbit = int(
        root.findall(".//sentinel-safe:relativeOrbitNumber")[0].text)
    
def fill_eo_properties(eo_ext, href):
    # Read meta file
    root = XmlElement.from_file(href)
    
    eo_ext.cloud_cover = float(
        root.find_attr("percentage", ".//sentinel3:cloudyPixels")
    )


def fill_proj_properties(proj_ext, meta_links, product_meta):
    """Fills the properties for SAR.

    Based on the sar Extension.py

    Args:
        input_ext (pystac.extensions.sar.SarExtension): The extension to be populated.
        href (str): The HREF to the scene, this is expected to be an XML file.

    Returns:
        pystac.Asset: An asset with the SAR relevant properties.
    """
    # Read meta file

    proj_ext.epsg = 4326

#     proj_ext.geometry = product_meta.geometry

    proj_ext.bbox = product_meta.bbox

    x_size = int(X_SIZE)
    y_size = int(Y_SIZE)

    proj_ext.shape = [x_size, y_size]
