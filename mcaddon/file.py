from typing import Self
from io import TextIOWrapper, BytesIO
from zipfile import ZipFile
from PIL import Image, ImageFile
from dataclasses import dataclass
import os
import chevron
import commentjson
import tempfile
import jsonschema

from . import APPDATA_PATH, EDU_APPDATA_PATH, PRE_APPDATA_PATH
from .exception import MinecraftNotFoundError, SchemaNotFoundError
from .constant import Edition
from .util import getattr2


class Schema:
    def __init__(self, schemafile: str, version: str = None):
        self.schemafile = schemafile
        self.version = version
        self.cache = None

    @property
    def schemafile(self) -> str:
        return getattr(self, "_schemafile")

    @schemafile.setter
    def schemafile(self, value: str):
        setattr(self, "_schemafile", str(value))

    @property
    def version(self) -> str | int:
        return getattr(self, "_version")

    @version.setter
    def version(self, value: str | int):
        setattr(self, "_version", value)

    def schema(self) -> dict:
        if self.cache is None:
            path = (
                self.schemafile
                if os.path.isabs(self.schemafile)
                else os.path.join(os.path.dirname(__file__), "schemas", self.schemafile)
            )
            with open(path, "r") as fd:
                self.cache = commentjson.load(fd)
        return self.cache

    def load(cls, self, data: dict):
        raise NotImplementedError()


class Loader:
    def __init__(self, cls, key: str = "format_version"):
        self.cls = cls
        self.key = key
        self.schemas = []

    @property
    def schemas(self) -> list[Schema]:
        return getattr2(self, "_schemas", [])

    @schemas.setter
    def schemas(self, value: list[Schema]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_schemas", value)

    @property
    def key(self) -> str:
        return getattr(self, "_key")

    @key.setter
    def key(self, value: str):
        setattr(self, "_key", str(value))

    @property
    def name(self) -> str:
        return getattr(self, "_name", "untitled")

    @name.setter
    def name(self, value: str):
        setattr(self, "_name", str(value))

    def get_schema(self, version: str | int) -> dict | None:
        """
        Get a JSON schema from the version

        :param version: The object version to get the schema for
        :type version: str | int
        """
        for s in self.schemas:
            if s.version == version:
                return s
        return None

    def add_schema(self, schema: Schema, version: str | int = None):
        """
        Add a new JSON schema to this loader for VERSION

        :param schema: The filename to the JSON schema
        :type schema: LoaderSchema
        """
        if not issubclass(schema, Schema):
            raise TypeError(
                f"Expected Schema but got '{schema.__class__.__name__}' instead"
            )
        schem = schema()
        if version is not None:
            schem.version = version
        self.schemas.append(schem)

    def clear_schemas(self):
        self.schemas = []

    def validate(self, data: dict, errors: bool = True) -> bool:
        """
        Validates this data

        :param data: The data to validate
        :type data: dict
        :param errors: If true it will raise errors if invalid, defaults to True
        :type errors: bool, optional
        """
        if self.key in data:
            version = data.get(self.key)
            s = self.get_schema(version)
            if s is not None:
                schema = s.schema()
                try:
                    # resolver = jsonschema.RefResolver(base_uri='file://'+os.path.dirname(__file__), store={})
                    jsonschema.validate(data, schema)
                    return True
                except jsonschema.ValidationError as err:
                    if errors:
                        raise SyntaxError(self.name, err.message)
                    return False
            if errors:
                raise SchemaNotFoundError(self.name, version)
        if errors:
            raise KeyError(self.key)
        return False

    def load(self, data: dict, errors: bool = True):
        cls = self.cls.__new__(self.cls)
        if self.key in data:
            version = data.get(self.key)
            s = self.get_schema(version)
            if s is not None:
                s.load(
                    cls, data.get(str(self.cls.id)) if hasattr(self.cls, "id") else data
                )
                return cls
            if errors:
                raise SchemaNotFoundError(version)
        if errors:
            raise KeyError(self.key)
        return None


class Importable:
    def import_to(self, edition: Edition = Edition.bedrock, dev: bool = True) -> str:
        """
        Saves this addon/pack to the correct Minecraft folders.

        :param edition: The Minecraft edition to import to, defaults to Edition.bedrock
        :type edition: Edition, optional
        :param dev: When True it will place this addon/pack in the development packs folders, defaults to True
        :type dev: bool, optional
        :return: The path to the imported addon/pack
        :rtype: str
        """
        # Bulid addon
        path = None
        match edition:
            case Edition.bedrock:
                path = APPDATA_PATH
            case Edition.preview:
                path = PRE_APPDATA_PATH
            case Edition.education:
                path = EDU_APPDATA_PATH
        if path is None:
            raise NotImplementedError("This platform is not supported")

        if not os.path.isdir(path):
            raise MinecraftNotFoundError(edition)
        return path

    def startfile(self) -> str:
        """
        Save this addon/pack and import to Minecraft, Like when you double click on a `.mcpack` file

        :return: The filepath to the built addon/pack that has been imported.
        :rtype: str
        """
        with tempfile.TemporaryFile(suffix=self.extension, delete=False) as tf:
            tf.write(self.getvalue())
            os.startfile(tf.name)
        return tf.name


class File:
    """
    Represents a File.
    """

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback) -> Self:
        self.save()

    @property
    def extension(self) -> str:
        return getattr(self, "_extension", self.EXTENSION)

    @extension.setter
    def extension(self, value: str):
        if value is None:
            delattr(self, "_extension")
            return
        setattr(self, "_extension", str(value))

    @property
    def filename(self) -> str:
        return getattr(self, "_filename", self.FILENAME)

    @filename.setter
    def filename(self, value: str):
        if value is None:
            delattr(self, "_filename")
            return
        setattr(self, "_filename", str(value))

    @property
    def dirname(self) -> str:
        return getattr(self, "_dirname", self.DIRNAME)

    @dirname.setter
    def dirname(self, value: str):
        if value is None:
            delattr(self, "_dirname")
            return
        setattr(self, "_dirname", str(value))

    @classmethod
    def from_fileobj(cls, fileobj: TextIOWrapper, args: dict[str, str]) -> Self:
        raise NotImplementedError()

    @classmethod
    def load(cls, filename: str, args={}):
        with open(filename, "r") as fileobj:
            self = cls.from_fileobj(fileobj, args)
            return self

    def has_filename(self) -> bool:
        return hasattr(self, "_filename")

    def write(self, fileobj: TextIOWrapper, **kw) -> Self:
        raise NotImplementedError()

    def save(self, filename: str = None, **kw) -> Self:
        if filename is None:
            filename = self.filename
        if filename is None:
            raise ValueError("No filename specified")

        # add extension if missing
        name, ext = os.path.splitext(filename)
        if name.endswith("/") or name.endswith("\\"):
            filename += self.FILENAME + self.extension
        elif ext == "":
            filename += self.extension

        dir = os.path.dirname(filename)
        if dir != "":
            os.makedirs(dir, exist_ok=True)
        with open(str(filename), "w") as fd:
            self.write(fd, **kw)
        return self

    def getvalue(self) -> bytes:
        with BytesIO() as io:
            self.write(io)
            return io.getvalue()


@dataclass(repr=False)
class JsonFile(File):
    """
    Represents a JSON File.
    """

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """
        Load object from DICT

        :param data: DICT data to load from
        :type data: dict
        """
        raise NotImplementedError()

    @classmethod
    def from_fileobj(cls, fileobj: TextIOWrapper, args: dict[str, str] = {}) -> Self:
        """
        Load object from FILEOBJ

        :param fileobj: The file to load
        :type fileobj: TextIOWrapper
        :param args: The arguments to pass to chevron to render
        :type args: dict[str, str]
        :rtype: JsonFile
        """
        text = chevron.render(fileobj, args, warn=True)
        self = cls.from_dict(commentjson.loads(text))
        self.filename = getattr(fileobj, "name", None)
        return self

    def json(self, **kw) -> str:
        """
        Convert object to a string in JSON format

        :return: Stringified JSON
        :rtype: str
        """
        return commentjson.dumps(self.__dict__, **kw)

    def write(self, fileobj: TextIOWrapper, indent: int = 2, **kw) -> int:
        """
        Write FILEOBJ as JSON

        :param fileobj: The file to write to
        :type fileobj: TextIOWrapper
        :param indent: The indentation for the JSON, defaults to 2
        :type indent: int, optional
        :return: _description_
        :rtype: int
        """
        return fileobj.write(self.json(indent=indent, **kw))


@dataclass(repr=False)
class PngFile(File):
    """
    Represents a PNG File.
    """

    image: ImageFile.ImageFile = None

    @classmethod
    def from_fileobj(cls, fileobj: TextIOWrapper) -> Self:
        self = cls.__new__(cls)
        self.image = Image.open(fileobj)
        self.filename = getattr(fileobj, "name", None)
        return self

    def write(self, fileobj: TextIOWrapper, indent: int = 2, **kw) -> int:
        return fileobj.write(self.json(indent=indent, **kw))


class ArchiveFile:
    """
    Represents an Archive File.
    """

    @classmethod
    def load(cls, filename: str = None) -> Self:
        self = cls.__new__(cls)
        if filename is not None:
            self.filename = filename
            if filename.startswith(".zip"):
                with ZipFile(filename) as zip:
                    return cls.readzip(zip)
        return cls.readdir(filename)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback) -> Self:
        self.save(zipped=False, overwrite=True)
        return self

    @property
    def extension(self) -> str:
        return getattr(self, "_extension", self.EXTENSION)

    @extension.setter
    def extension(self, value: str):
        if value is None:
            delattr(self, "_extension")
            return
        setattr(self, "_extension", str(value))

    @property
    def filename(self) -> str:
        return getattr(self, "_filename", self.FILENAME)

    @filename.setter
    def filename(self, value: str):
        if value is None:
            delattr(self, "_filename")
            return
        setattr(self, "_filename", os.path.realpath(value))

    @classmethod
    def readzip(cls, zip: ZipFile) -> Self:
        raise NotImplementedError()

    @classmethod
    def readdir(cls, path: str) -> Self:
        raise NotImplementedError()

    def has_filename(self) -> bool:
        return hasattr(self, "_filename")

    def save(
        self, filename: str = None, zipped: bool = False, overwrite: bool = False
    ) -> Self:
        if filename is None:
            filename = self.filename
        if filename is None:
            raise ValueError("No path specified")

        # add extension if missing
        name, ext = os.path.splitext(filename)
        if name.endswith("/") or name.endswith("\\"):
            filename += self.FILENAME + self.extension
        elif ext == "":
            filename += self.extension

        # Make dir
        dir = os.path.dirname(filename)
        if dir != "":
            os.makedirs(dir, exist_ok=True)

        if zipped:
            if os.path.exists(filename) and not overwrite:
                raise FileExistsError(f"Could't overwrite {filename!r}")
            with ZipFile(filename, "w") as zip:
                self.writezip(zip)
            return self
        else:
            filename, ext = os.path.splitext(filename)
            if not overwrite:
                c = 1
                while os.path.exists(filename):
                    filename = filename + str(c)
                    c += 1
            self.writedir(filename)
        return self

    def writedir(self, path: str) -> Self:
        raise NotImplementedError()

    def writezip(self, zip: ZipFile) -> Self:
        raise NotImplementedError()

    def getvalue(self) -> bytes:
        with BytesIO() as io:
            with ZipFile(io, "w") as zip:
                self.writezip(zip)
            return io.getvalue()

    def setup(self): ...
