__all__ = ["File", "TextFile", "BinaryFile", "JsonFile", "NbtFile", "ResourceFile"]

from typing import ClassVar, Dict, Any, Optional, cast
from abc import ABC, abstractmethod
from io import TextIOWrapper, BufferedReader, BufferedWriter
from pydantic import BaseModel as _BaseModel, ConfigDict
from pathlib import Path
from rapidnbt import nbtio
from mcaddon import __format_version__
import commentjson
import os

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

from .base import BaseModel
from .utils import convert_sets


class File(ABC):
    extension: ClassVar[str]

    def __enter__(self) -> Self:
        return self

    def __exit__(self, a, b, c) -> None:
        if self.filepath is not None and "w" in self.mode:
            self.save(self.filepath)

    @classmethod
    def open(cls, file: str, mode: str = "r") -> Self:
        return cls.__new__(cls)

    @property
    def startpath(self) -> Optional[str]:
        return getattr(self, "_startpath", None)

    @property
    def filepath(self) -> Optional[str]:
        return getattr(self, "_filepath", None)

    @property
    def mode(self) -> str:
        return getattr(self, "_mode", "r")

    def save(self, file: str) -> None:
        pass


class TextFile(File, ABC):

    @classmethod
    def open(cls, file: str | Path, mode: str = "r", encoding: str = "utf-8") -> Self:
        if "r" in mode:
            with open(file, "r", encoding=encoding) as f:
                res = cls.load(f)
                setattr(res, "_filepath", file)
                setattr(res, "_mode", mode)
                return res
        return cls.__new__(cls)

    def save(self, file: str, *args, **kw) -> None:
        # Create directory
        dir = os.path.dirname(file)
        if dir:
            os.makedirs(dir, exist_ok=True)
        # Save file
        with open(file, "w") as f:
            self.dump(f, *args, **kw)

    @classmethod
    def load(cls, obj: TextIOWrapper, *args, **kw) -> Self:
        return cls.loads(obj.read(), *args, **kw)

    def dump(self, fp: TextIOWrapper, *args, **kw) -> None:
        fp.write(self.dumps(*args, **kw))

    # OVERRIDE

    @classmethod
    @abstractmethod
    def loads(cls, obj: str, *args, **kw) -> Self:
        pass

    @abstractmethod
    def dumps(self, *args, **kw) -> str:
        pass


class BinaryFile(File, ABC):

    @classmethod
    def open(cls, file: str | Path, mode: str = "r") -> Self:
        if "r" in mode:
            with open(file, "rb") as f:
                res = cls.load(f)
                setattr(res, "_filepath", file)
                setattr(res, "_mode", mode)
                return res
        return cls.__new__(cls)

    def save(self, file) -> None:
        with open(file, "wb") as f:
            self.dump(f)

    @classmethod
    def load(cls, obj: BufferedReader, *args, **kw) -> Self:
        return cls.loads(obj.read(), *args, **kw)

    def dump(self, fp: BufferedWriter, *args, **kw) -> None:
        fp.write(self.dumps(), *args, **kw)

    # OVERRIDE

    @classmethod
    @abstractmethod
    def loads(cls, obj: bytes, *args, **kw) -> Self:
        pass

    @abstractmethod
    def dumps(self, *args, **kw) -> bytes:
        pass


class NbtFile(BinaryFile, BaseModel):
    extension: ClassVar[str] = ".nbt"

    @classmethod
    def loads(cls, obj: bytes, *args, **kw) -> Self:
        nbt = nbtio.loads(obj)
        if not nbt:
            raise Exception("Not an NBT file!")
        return cls.model_validate_json(nbt.to_json())

    def dumps(self, *args, **kw) -> bytes:
        json = self.model_dump_json(*args, **kw)
        a = nbtio.loads_json(json)
        if not a:
            raise Exception("Failed to serilize nbt!")
        return bytes(nbtio.dumps(a))


class JsonFile(TextFile, _BaseModel):
    extension: ClassVar[str] = ".json"

    @property
    def id(self) -> str:
        if not self.filepath or not self.startpath:
            return "empty"

        parts = Path(self.filepath).parts
        idx = parts.index(self.startpath)
        return str(Path(*parts[idx:]))

    @classmethod
    def loads(cls, obj: str) -> "JsonFile":
        obj = obj.lstrip("\ufeff")  # remove BOM
        return cls.model_validate(commentjson.loads(obj))

    def dumps(self, indent=2, exclude_none: bool = True, *args, **kw) -> str:
        return self.model_dump_json(
            indent=indent, exclude_none=exclude_none, *args, **kw
        )


class ResourceFile(JsonFile):
    model_config: ClassVar[ConfigDict] = ConfigDict()
    TYPE_ID: ClassVar[str] = "minecraft:resource"
    format_version: str = __format_version__

    def __hash__(self) -> int:
        return hash(self.TYPE_ID)

    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        """Dump format_version outside KEY."""
        if "exclude_none" not in kwargs:
            kwargs["exclude_none"] = True
        data = super().model_dump(*args, **kwargs)
        resource = {k: v for k, v in data.items() if k != "format_version"}
        return cast(
            Dict[str, Any],
            convert_sets(
                {"format_version": self.format_version, self.TYPE_ID: resource}
            ),
        )

    def model_dump_json(self, indent=0, separators=(",", ": "), *args, **kwargs) -> str:
        if "exclude_none" not in kwargs:
            kwargs["exclude_none"] = True
        obj = self.model_dump(*args, **kwargs)
        return str(commentjson.dumps(obj, indent=indent, separators=separators))

    @classmethod
    def model_validate(cls, obj, strict=True, *args, **kwargs) -> Self:
        """Validate with format_version outside KEY."""
        if isinstance(obj, dict) and cls.TYPE_ID in obj:
            resource = dict(obj[cls.TYPE_ID])
            if "format_version" in obj:
                resource["format_version"] = obj["format_version"]
            obj = resource
        return super().model_validate(obj, strict=strict, *args, **kwargs)
