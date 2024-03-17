from typing import Self
from io import TextIOWrapper, BytesIO
from PIL import Image, ImageFile
from dataclasses import dataclass
import os
import chevron
import commentjson
import tempfile
import jsonschema
import zipfile
import tarfile

from . import APPDATA_PATH, EDU_APPDATA_PATH, PRE_APPDATA_PATH
from .exception import MinecraftNotFoundError, SchemaNotFoundError, SyntaxError
from .constant import Edition
from .util import getattr2, splitpath, modpath, Misc, Identifiable, Identifier


class Schema:
    def __init__(self, schemafile: str, version: str = None):
        self.schemafile = schemafile
        self.version = version
        self.cache = None

    @property
    def schemafile(self) -> str:
        """The filepath to this JSON schema."""
        return getattr(self, "_schemafile")

    @schemafile.setter
    def schemafile(self, value: str):
        setattr(self, "_schemafile", str(value))

    @property
    def version(self) -> str | int:
        """The version to match."""
        return getattr(self, "_version")

    @version.setter
    def version(self, value: str | int):
        setattr(self, "_version", value)

    def schema(self) -> dict:
        """Get the JSON schema file and cache for future use."""
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
        """All schemas registered to this loader."""
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
        """The root key required for this object."""
        return getattr(self, "_key")

    @key.setter
    def key(self, value: str):
        setattr(self, "_key", str(value))

    @property
    def name(self) -> str:
        """The display name of this loader for errors."""
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
        """Remove all schemas"""
        self.schemas = []

    def validate(self, data: dict, errors: bool = True) -> bool:
        """
        Validates this data

        :param data: The data to validate
        :type data: dict
        :param errors: If true it will raise errors if invalid, defaults to True
        :type errors: bool, optional
        """
        obj = data.copy()
        if self.key in obj:
            version = obj.get(self.key)
            s = self.get_schema(version)
            if s is not None:
                schema = s.schema()
                try:
                    # resolver = jsonschema.RefResolver(base_uri='file://'+os.path.dirname(__file__), store={})
                    jsonschema.validate(obj, schema)
                    return True
                except jsonschema.ValidationError as err:
                    if errors:
                        raise SyntaxError(self.name, err.message, s.schemafile)
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
    def import_to(
        self, name: str = None, edition: Edition = Edition.BEDROCK, dev: bool = True
    ) -> str:
        """
        Saves this addon/pack to the correct Minecraft folders.

        :param edition: The Minecraft edition to import to, defaults to Edition.BEDROCK
        :type edition: Edition, optional
        :param dev: When True it will place this addon/pack in the development packs folders, defaults to True
        :type dev: bool, optional
        :return: The path to the imported addon/pack
        :rtype: str
        """
        # Bulid addon
        path = None
        match edition:
            case Edition.BEDROCK:
                path = APPDATA_PATH
            case Edition.PREVIEW:
                path = PRE_APPDATA_PATH
            case Edition.EDUCATION:
                path = EDU_APPDATA_PATH
        if path is None:
            raise NotImplementedError("This platform is not supported")
        if name is not None:
            self.filename = name

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


class File(Misc):
    """Represents a File."""

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback) -> Self:
        self.save()

    @property
    def fp(self) -> str:
        """This objects path on disk"""
        return getattr(self, "_fp", self.FILEPATH)

    @fp.setter
    def fp(self, value: str):
        setattr(self, "_fp", os.path.join(value))

    @property
    def extension(self) -> str:
        """This objects extension from fp"""
        return splitpath(self.fp)[2]

    @extension.setter
    def extension(self, value: str):
        self.fp = modpath(self.fp, "e", value)

    @property
    def filename(self) -> str:
        """This objects name from fp"""
        return splitpath(self.fp)[1]

    @filename.setter
    def filename(self, value: str):
        self.fp = modpath(self.fp, "f", value)

    @property
    def dirname(self) -> str:
        """This objects directory from fp"""
        return splitpath(self.fp)[0]

    @dirname.setter
    def dirname(self, value: str):
        self.fp = modpath(self.fp, "d", value)

    @classmethod
    def from_fileobj(cls, fileobj: TextIOWrapper, args: dict[str, str]) -> Self:
        raise NotImplementedError()

    @classmethod
    def open(cls, file: str, start: str = None):
        """
        Open a FILE to load

        :param file: The path to a DIRECTORY or ARCHIVE FILE to open
        :type file: str
        """
        with open(file, "r") as fd:
            obj = cls.load(fd)
            obj.filename = os.path.basename(file)
            dirname = os.path.dirname(os.path.relpath(file, start))
            if dirname is not None and dirname != "" and dirname != " ":
                obj.dirname = os.path.join(obj.dirname, dirname)
            return obj

    @classmethod
    def loads(cls, s: str) -> Self:
        raise NotImplementedError()

    @classmethod
    def load(cls, fileobj: TextIOWrapper) -> Self:
        """
        Deserialize fp (a .read()-supporting file-like object) to a Python object.
        """
        return cls.loads(fileobj.read())

    def dump(self, fileobj: TextIOWrapper):
        """
        Serialize obj as a formatted stream to fp (a .write()-supporting file-like object).
        """
        fileobj.write(bytes(self.dumps(), "utf-8"))

    def dumps(self) -> str:
        raise NotImplementedError()

    def save(self, fp: str = None, overwrite: bool = True, **kw) -> Self:
        """
        Save this object to disk.

        :param fp: The filepath to save, defaults to None
        :type fp: str, optional
        :param overwrite: When true it will override the previus written file. When false it will not override the file, defaults to True
        :type overwrite: bool, optional
        """
        fp = self.filename if fp is None else fp
        if fp is None:
            raise ValueError("No filename specified")

        # add extension if missing
        name, ext = os.path.splitext(fp)
        if name.endswith("/") or name.endswith("\\"):
            fp += self.filename + self.extension
        elif ext == "":
            fp += self.extension

        dir = os.path.dirname(fp)
        if dir != "":
            os.makedirs(dir, exist_ok=True)
        with open(str(fp), "wb") as fd:
            return self.dump(fd)

    def valid(self, fp: str) -> bool:
        return True

    def getvalue(self) -> bytes:
        """
        :rtype: bytes
        """
        with BytesIO() as io:
            self.dump(io)
            return io.getvalue()


@dataclass(repr=False)
class JsonFile(File):
    """
    Represents a JSON File.
    """

    def __eq__(self, other) -> bool:
        # if isinstance(other, JsonFile): Super Slow
        #     return self.jsonify() == other.jsonify()
        if isinstance(self, Identifiable) and isinstance(
            other, (str, Identifier, Identifiable)
        ):
            return self.identifier == Identifiable.of(other)
        return False

    def __len__(self) -> int:
        return len(self.__dict__)

    def __contains__(self, item) -> bool:
        if hasattr(self, item):
            value = getattr(self, item)
            if isinstance(value, (dict, list, set)):
                return True if value else False
            return value is not None
        return False

    # TODO: Handle nested values. ex: 'main.nested' == {main: {nested: 5}}}
    def __setitem__(self, name: str, value) -> None:
        setattr(self, name, value)

    def __getitem__(self, name: str):
        return getattr(self, name)

    def __delitem__(self, name: str) -> None:
        delattr(self, name)

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """
        Load object from DICT

        :param data: DICT data to load from
        :type data: dict
        """
        raise NotImplementedError()

    @classmethod
    def jsonfile(cls, fp: str) -> dict:
        """Opens fp and returns the result as JSON"""
        with open(fp, "r") as fd:
            return commentjson.load(fd)

    @classmethod
    def load(cls, fileobj: TextIOWrapper, args: dict[str, str] = {}) -> Self:
        """Deserialize fp (a .read()-supporting file-like object containing a JSON document) to a Python object."""
        text = chevron.render(fileobj.read(), args, warn=True)
        self = cls.from_dict(commentjson.loads(text))
        self.filename = getattr(fileobj, "name", None)
        return self

    @classmethod
    def loads(cls, s: str, args: dict[str, str] = {}) -> Self:
        """Deserialize s (a str, bytes or bytearray instance containing a JSON document) to a Python object."""
        text = chevron.render(s, args, warn=True)
        self = cls.from_dict(commentjson.loads(text))
        return self

    def dumps(self, indent: int = 2, **kw) -> str:
        """Serialize obj to a JSON formatted str."""
        return commentjson.dumps(self.jsonify(), indent=indent, **kw)

    def valid(self, fp: str) -> bool:
        """
        Whether or not this is a valid object

        :param fp: The FILE to validate
        :type fp: str
        :rtype: bool
        """
        data = self.jsonfile(fp)
        return str(self.id) in data

    def copy(self) -> Self:
        return self.from_dict(self.jsonify())

    def generate(self, ctx) -> None:
        """
        Called when this object is added to BehaviorPack or ResourcePack

        :type ctx: BehaviorPack | ResourcePack
        """
        ...

    @staticmethod
    def from_dict(data: dict) -> Self:
        raise NotImplementedError()

    def jsonify(self) -> dict:
        raise NotImplementedError()


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


class ArchiveFile(Misc):
    """
    Represents an Archive File.
    """

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback) -> Self:
        self.save(zipped=False, overwrite=True)
        return self

    @property
    def fp(self) -> str:
        """This objects path on disk"""
        return getattr(self, "_fp", self.FILEPATH)

    @fp.setter
    def fp(self, value: str):
        setattr(self, "_fp", os.path.join(value))

    @property
    def extension(self) -> str:
        """This objects extension from fp"""
        return splitpath(self.fp)[2]

    @extension.setter
    def extension(self, value: str):
        self.fp = modpath(self.fp, "e", value)

    @property
    def filename(self) -> str:
        """This objects name from fp"""
        return splitpath(self.fp)[1]

    @filename.setter
    def filename(self, value: str):
        self.fp = modpath(self.fp, "f", value)

    @property
    def dirname(self) -> str:
        """This objects directory from fp"""
        return splitpath(self.fp)[0]

    @dirname.setter
    def dirname(self, value: str):
        self.fp = modpath(self.fp, "d", value)

    # new

    @classmethod
    def open(cls, file: str, *args, **kw) -> Self:
        """
        Open a ZIP, TAR, or DIRECTORY to load

        :param file: The path to a DIRECTORY or ARCHIVE FILE to open
        :type file: str
        """
        try:
            if zipfile.is_zipfile(file):
                with zipfile.ZipFile(file, "r") as fd:
                    obj = cls.load_archive(fd, *args, **kw)
            elif tarfile.is_tarfile(file):
                with tarfile.open(file, "r") as tf:
                    obj = cls.load_archive(tf, *args, **kw)

            obj.dirname = os.path.dirname(file)
            obj.filename, ext = os.path.splitext(os.path.basename(file))
            return obj
        except PermissionError:
            obj = cls.load_directory(file, *args, **kw)
            obj.dirname = os.path.dirname(file)
            obj.filename, ext = os.path.splitext(os.path.basename(file))
            return obj

    @classmethod
    def load_archive(cls, fileobj: zipfile.ZipFile, *args, **kw) -> Self:
        raise NotImplementedError()

    @classmethod
    def load_directory(cls, path: str, *args, **kw) -> Self:
        raise NotImplementedError()

    def dump_archive(self, fileobj: zipfile.ZipFile, *args, **kw):
        raise NotImplementedError()

    def dump_directory(self, path: str, *args, **kw):
        raise NotImplementedError()

    def save(
        self, fp: str = None, zipped: bool = False, overwrite: bool = False, *args, **kw
    ):
        """
        Save this object to disk.

        :param fp: The filepath to save, defaults to None
        :type fp: str, optional
        :param zipped: When true it will save as a ZIP file. When false save in FOLDER, defaults to False
        :type zipped: bool, optional
        :param overwrite: When true it will override the previus written file. When false it will not override the file, defaults to False
        :type overwrite: bool, optional
        """
        fp = self.fp if fp is None else fp
        if fp is None:
            raise ValueError("No filename specified")
        self.fp = fp

        # Make unique filename if overrite=False and exits
        if not overwrite and os.path.exists(fp):
            c = 0
            while not os.path.exists(fp):
                t, ext = os.path.splitext(fp)
                fp = t + str(c) + ext
                c += 1

        if zipped:
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            with zipfile.ZipFile(fp, "w") as zf:
                return self.dump_archive(zf, *args, **kw)
        return self.dump_directory(
            os.path.join(self.dirname, self.filename), *args, **kw
        )

    def valid(self, fp: str) -> bool:
        """
        Whether or not this is a valid object

        :param fp: The DIRECTORY, TAR file or ZIP file to validate
        :type fp: str
        :rtype: bool
        """
        try:
            return tarfile.is_tarfile(fp) or zipfile.is_zipfile(fp)  # TAR or ZIP file
        except PermissionError:
            return True  # Directory

    def getvalue(self) -> bytes:
        """
        :rtype: bytes
        """
        with BytesIO() as io:
            with zipfile.ZipFile(io, "w") as zf:
                self.dump_archive(zf)
            return io.getvalue()
