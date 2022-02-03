from typing import List, Optional

import pystac
from pystac.extensions.file import ByteOrder, FileExtension, MappingObject

LOCAL_PATH_PROP = "file:local_path"


class FileExtensionUpdated(FileExtension):
    SCHEMA_URI = "https://stac-extensions.github.io/file/v2.1.0/schema.json"

    def apply(self,
              byte_order: Optional[ByteOrder] = None,
              checksum: Optional[str] = None,
              header_size: Optional[int] = None,
              size: Optional[int] = None,
              values: Optional[List[MappingObject]] = None,
              local_path: Optional[str] = None) -> None:
        super().apply(byte_order, checksum, header_size, size, values)
        self.local_path = local_path

    @property
    def local_path(self) -> Optional[str]:
        """Get or sets the local path of the file."""
        return self._get_property(LOCAL_PATH_PROP, str)

    @local_path.setter
    def local_path(self, v: Optional[str]) -> None:
        self._set_property(LOCAL_PATH_PROP, v)

    @classmethod
    def ext(cls,
            obj: pystac.Asset,
            add_if_missing: bool = False) -> "FileExtensionUpdated":
        super().ext(obj, add_if_missing)
        return cls(obj)

    @classmethod
    def get_schema_uri(cls) -> str:
        return cls.SCHEMA_URI
