from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class FileName:
    """Dataclass for parsing sentinel3 file names.

    Based on the naming convention docs:

    - https://sentinel.esa.int/web/sentinel/user-guides/sentinel-3-olci/naming-convention
    - https://sentinel.esa.int/web/sentinel/user-guides/sentinel-3-slstr/naming-convention
    - https://sentinel.esa.int/web/sentinel/user-guides/sentinel-3-synergy/naming-conventions
    """

    mission_id: str
    data_source: str
    processing_level: Optional[int]
    data_type_id: str
    sensing_start_time: str
    sensing_stop_time: str
    product_creation_date: str
    instance_id: str
    centre: str
    class_id: str

    @classmethod
    def from_str(cls, s: str) -> FileName:
        """Creates a file name from a string.

        The string should be the file name, with or without the .SEN3 extension.
        """
        if len(s) < 95:
            raise ValueError(
                f"file name is too short (should be at least 95 characters): {s}"
            )
        try:
            processing_level = int(s[7])
        except ValueError:
            processing_level = None
        return cls(
            mission_id=s[0:3].strip("_"),
            data_source=s[4:6],
            processing_level=processing_level,
            data_type_id=s[9:15].strip("_"),
            sensing_start_time=s[16:31],
            sensing_stop_time=s[32:47],
            product_creation_date=s[48:63],
            instance_id=s[64:81].strip("_"),
            centre=s[82:85],
            class_id=s[86:94],
        )

    @property
    def scene_id(self) -> str:
        """Returns a scene id, used as the item id."""
        if self.processing_level is None:
            raise ValueError("can't create a scene id without a processing level")
        else:
            return (
                f"{self.mission_id}_{self.data_source}_{self.processing_level}_"
                f"{self.data_type_id}_{self.sensing_start_time}_{self.sensing_stop_time}_"
                + self.instance_id
            )
