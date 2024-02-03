from typing import Self
from uuid import uuid4, UUID

from . import VERSION
from .constant import ModuleType
from .file import JsonFile, Loader
from .util import getattr2, Version


class Header:
    def __init__(
        self,
        min_engine_version: Version = None,
        name: str = None,
        description: str = None,
        uuid: UUID = None,
        version: Version = None,
        allow_random_seed: bool = None,
        base_game_version: Version = None,
        lock_template_options: bool = None,
    ):
        self.name = name
        self.uuid = uuid
        self.description = description
        self.version = version
        self.allow_random_seed = allow_random_seed
        self.base_game_version = base_game_version
        self.lock_template_options = lock_template_options
        self.min_engine_version = min_engine_version

    @property
    def __dict__(self) -> dict:
        data = {
            "name": self.name_key,
            "description": self.description_key,
            "uuid": str(self.uuid),
            "version": self.version.__dict__,
            "min_engine_version": self.min_engine_version.__dict__,
        }
        if self.allow_random_seed:
            data["allow_random_seed"] = self.allow_random_seed
        if self.base_game_version:
            data["base_game_version"] = self.base_game_version.__dict__
        if self.lock_template_options:
            data["lock_template_options"] = self.lock_template_options
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.name = data.pop("name")
        self.description = data.pop("description")
        self.uuid = data.pop("uuid")
        self.version = data.pop("version")
        if "allow_random_seed" in data:
            self.allow_random_seed = data.pop("allow_random_seed")
        if "base_game_version" in data:
            self.base_game_version = data.pop("base_game_version")
        if "lock_template_options" in data:
            self.lock_template_options = data.pop("lock_template_options")
        if "min_engine_version" in data:
            self.min_engine_version = data.pop("min_engine_version")
        return self

    @property
    def name_key(self) -> str:
        return getattr(self, "_name_key", "pack.name")

    @name_key.setter
    def name_key(self, value: str):
        if value is None:
            self.name_key = "pack.name"
        else:
            setattr(self, "_name_key", str(value))

    @property
    def description_key(self) -> str:
        return getattr(self, "_description_key", "pack.description")

    @description_key.setter
    def description_key(self, value: str):
        if value is None:
            self.description_key = "pack.description"
        else:
            setattr(self, "_description_key", str(value))

    @property
    def name(self) -> str:
        return getattr(self, "_name", "Untitled")

    @name.setter
    def name(self, value: str):
        if value is None:
            self.name = "Untitled"
            return
        setattr(self, "_name", str(value))

    @property
    def description(self) -> str:
        return getattr(self, "_description", "Auto generated")

    @description.setter
    def description(self, value: str):
        if value is None:
            self.description = "Auto generated"
            return
        setattr(self, "_description", str(value))

    @property
    def min_engine_version(self) -> Version:
        return getattr2(
            self, "_min_engine_version", Version.parse(VERSION["MIN_ENGINE_VERSION"])
        )

    @min_engine_version.setter
    def min_engine_version(self, value: Version):
        if value is None:
            self.min_engine_version = Version.parse(VERSION["MIN_ENGINE_VERSION"])
            return
        if not isinstance(value, Version):
            raise TypeError(
                f"Expected Version but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_min_engine_version", value)

    @property
    def uuid(self) -> UUID:
        return getattr(self, "_uuid", uuid4())

    @uuid.setter
    def uuid(self, value: UUID):
        if value is None:
            self.uuid = uuid4()
        elif isinstance(value, UUID):
            setattr(self, "_uuid", value)
        else:
            self.uuid = UUID(str(value))

    @property
    def version(self) -> Version:
        return getattr(self, "_version", Version(1, 0, 0))

    @version.setter
    def version(self, value: Version):
        if value is None:
            self.version = Version(1, 0, 0)
            return
        if not isinstance(value, Version):
            raise TypeError(
                f"Expected Version but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_version", value)

    @property
    def allow_random_seed(self) -> bool:
        return getattr(self, "_allow_random_seed", False)

    @allow_random_seed.setter
    def allow_random_seed(self, value: bool):
        if value is None:
            self.allow_random_seed = False
            return
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_allow_random_seed", value)

    @property
    def base_game_version(self) -> Version | None:
        return getattr(self, "_base_game_version", None)

    @base_game_version.setter
    def base_game_version(self, value: Version):
        if value is None:
            setattr(self, "_base_game_version", None)
            return
        if not isinstance(value, Version):
            raise TypeError(
                f"Expected Version but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_base_game_version", value)

    @property
    def lock_template_options(self) -> bool:
        return getattr(self, "_lock_template_options", False)

    @lock_template_options.setter
    def lock_template_options(self, value: bool):
        if value is None:
            self.lock_template_options = False
            return
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_lock_template_options", value)


class Metadata:
    def __init__(self, license: str, url: str):
        self.authors = []
        self.license = license
        self.url = url

    @property
    def __dict__(self) -> dict:
        data = {"authors": self.authors, "license": self.license, "url": self.url}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.authors = data.pop("authors")
        self.license = data.pop("license")
        self.url = data.pop("url")
        return self

    @property
    def authors(self) -> list[str]:
        return getattr(self, "_authors")

    @authors.setter
    def authors(self, value: list[str]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_authors", value)

    @property
    def license(self) -> str:
        return getattr(self, "_license")

    @license.setter
    def license(self, value: str):
        setattr(self, "_license", str(value))

    @property
    def url(self) -> str:
        return getattr(self, "_url")

    @url.setter
    def url(self, value: str):
        setattr(self, "_url", str(value))

    def add_author(self, name: str) -> str:
        self.authors.append(name)
        return name

    def get_author(self, index: int) -> str:
        return self.authors[index]

    def remove_author(self, index: int) -> str:
        name = self.authors[index]
        del self.authors[index]
        return name

    def clear_authors(self):
        self.authors = []
        return self


class Dependency:
    def __init__(self, uuid: UUID, version: list[int] = None):
        self.uuid = uuid
        self.version = version

    @property
    def __dict__(self) -> dict:
        data = {"uuid": str(self.uuid), "version": self.version.__dict__}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.uuid = data.pop("uuid")
        self.version = data.pop("version")
        return self

    @property
    def uuid(self) -> UUID:
        return getattr(self, "_uuid")

    @uuid.setter
    def uuid(self, value: UUID):
        if isinstance(value, UUID):
            setattr(self, "_uuid", value)
        else:
            self.uuid = UUID(str(value))

    @property
    def version(self) -> Version:
        return getattr(self, "_version", Version(1, 0, 0))

    @version.setter
    def version(self, value: Version):
        if value is None:
            self.version = Version(1, 0, 0)
            return
        if not isinstance(value, Version):
            raise TypeError(
                f"Expected Version but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_version", value)


class Module:
    def __init__(
        self,
        type: ModuleType,
        uuid: str = None,
        version: list[int] = None,
        description: str = None,
    ):
        self.type = type
        self.description = description
        self.uuid = uuid
        self.version = version

    @property
    def __dict__(self) -> dict:
        data = {
            "description": self.description,
            "type": self.type._value_,
            "uuid": str(self.uuid),
            "version": self.version.__dict__,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.description = data.pop("description")
        self.type = ModuleType[data.pop("type")]
        self.uuid = data.pop("uuid")
        self.version = data.pop("version")
        return self

    @property
    def type(self) -> ModuleType:
        return getattr(self, "_type")

    @type.setter
    def type(self, value: ModuleType):
        if not isinstance(value, ModuleType):
            raise TypeError(
                f"Expected ModuleType but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_type", value)

    @property
    def description(self) -> str:
        return getattr(self, "_description", "pack.description")

    @description.setter
    def description(self, value: str):
        if value is None:
            self.description = "pack.description"
        else:
            setattr(self, "_description", str(value))

    @property
    def uuid(self) -> UUID:
        return getattr2(self, "_uuid", uuid4())

    @uuid.setter
    def uuid(self, value: UUID):
        if value is None:
            self.uuid = uuid4()
        elif isinstance(value, UUID):
            setattr(self, "_uuid", value)
        else:
            self.uuid = UUID(str(value))

    @property
    def version(self) -> Version:
        return getattr(self, "_version", Version(1, 0, 0))

    @version.setter
    def version(self, value: Version):
        if value is None:
            self.version = Version(1, 0, 0)
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_version", value)

    @classmethod
    def resources(cls, uuid: UUID = None) -> Self:
        self = cls.__new__(cls)
        self.type = ModuleType.resources
        self.uuid = uuid
        return self

    @classmethod
    def data(cls, uuid: UUID = None) -> Self:
        self = cls.__new__(cls)
        self.type = ModuleType.data
        self.uuid = uuid
        return self

    @classmethod
    def client_data(cls, uuid: UUID = None) -> Self:
        self = cls.__new__(cls)
        self.type = ModuleType.client_data
        self.uuid = uuid
        return self

    @classmethod
    def interface(cls, uuid: UUID = None) -> Self:
        self = cls.__new__(cls)
        self.type = ModuleType.interface
        self.uuid = uuid
        return self

    @classmethod
    def world_template(cls, uuid: UUID = None) -> Self:
        self = cls.__new__(cls)
        self.type = ModuleType.world_template
        self.uuid = uuid
        return self


class Manifest(JsonFile):
    """
    Represents a Pack Manifest.
    """

    EXTENSION = ".json"
    DIRNAME = ""
    FILENAME = "manifest"

    def __init__(self, header: Header, metadata: Metadata = None):
        self.header = header
        self.metadata = metadata
        self.dependencies = {}
        self.modules = {}

    def __iter__(self):
        for i in self.modules:
            yield i

    def __str__(self):
        return "Manifest{" + str(self.header.uuid) + "}"

    @property
    def __dict__(self) -> dict:
        data = {
            "format_version": VERSION["MANIFEST"],
            "header": self.header.__dict__,
            "modules": [],
        }

        if self.metadata:
            data["metadata"] = self.metadata.__dict__

        if self.dependencies:
            data["dependencies"] = []
            for v in self.dependencies.values():
                data["dependencies"].append(v.__dict__)
        if self.modules:
            for v in self.modules.values():
                data["modules"].append(v.__dict__)
        return data

    @property
    def header(self) -> Header:
        return getattr(self, "_header")

    @header.setter
    def header(self, value: Header):
        if not isinstance(value, Header):
            raise TypeError(
                f"Expected Header but got '{value.__class__.__name__}' instead"
            )
        self.FILENAME = value.name
        setattr(self, "_header", value)

    @property
    def metadata(self) -> Metadata:
        return getattr(self, "_metadata", None)

    @metadata.setter
    def metadata(self, value: Metadata):
        if value is None:
            setattr(self, "_metadata", None)
            return
        if not isinstance(value, Metadata):
            raise TypeError(
                f"Expected Metadata but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_metadata", value)

    @property
    def dependencies(self) -> dict[str, Dependency]:
        return getattr(self, "_dependencies", {})

    @dependencies.setter
    def dependencies(self, value: dict[str, Dependency]):
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_dependencies", value)

    @property
    def modules(self) -> dict[str, Module]:
        return getattr(self, "_modules", {})

    @modules.setter
    def modules(self, value: dict[str, Module]):
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_modules", value)

    # SHORTCUTS

    @property
    def name(self) -> str:
        return self.header.name

    @name.setter
    def name(self, value: str):
        self.header.name = value

    @property
    def description(self) -> str:
        return self.header.description

    @description.setter
    def description(self, value: str):
        self.header.description = value

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = ManifestLoader()
        loader.validate(data)
        return loader.load(data)

    def add_module(self, module: Module) -> Module:
        self.modules[module.uuid] = module
        return module

    def set_module(self, module: Module) -> Module:
        self.clear_modules()
        return self.add_module(module)

    def get_module(self, uuid: str) -> Module:
        return self.modules[uuid]

    def remove_module(self, uuid: str) -> Module:
        return self.modules.pop(uuid)

    def clear_modules(self) -> Self:
        self.modules = {}
        return self

    def add_dependency(self, obj: Dependency | Self) -> Dependency:
        from .pack import Pack

        if isinstance(obj, Manifest):
            return self.add_dependency(Dependency(obj.header.uuid, obj.header.version))
        elif isinstance(obj, Pack):
            return self.add_dependency(
                Dependency(obj.manifest.header.uuid, obj.manifest.header.version)
            )
        if not isinstance(obj, Dependency):
            raise TypeError(
                f"Expected Dependency but got '{obj.__class__.__name__}' instead"
            )
        self.dependencies[obj.uuid] = obj
        return obj

    def get_dependency(self, uuid: str) -> Dependency:
        return self.dependencies[uuid]

    def remove_dependency(self, uuid: str) -> Dependency:
        return self.dependencies.pop(uuid)

    def clear_dependencies(self) -> Self:
        self.dependencies = {}
        return self

    def set_uuids(self, header_uuid: str, *module_uuid: str) -> Self:
        self.header.uuid = header_uuid
        for idx, uuid in enumerate(module_uuid):
            m = list(self.modules.values())[idx]
            m.uuid = uuid
        return self

    @classmethod
    def behavior(cls) -> Self:
        self = cls.__new__(cls)
        self.modules = {}
        self.dependencies = {}
        self.header = Header()
        self.add_module(Module.data())
        return self

    @classmethod
    def resource(cls) -> Self:
        self = cls.__new__(cls)
        self.modules = {}
        self.dependencies = {}
        self.header = Header()
        self.add_module(Module.resources())
        return self

    @classmethod
    def world_template(cls) -> Self:
        self = cls.__new__(cls)
        self.modules = {}
        self.dependencies = {}
        self.header = Header()
        self.add_module(Module.world_template())
        return self


class ManifestLoader(Loader):
    name = "Manifest"

    def __init__(self):
        from .schemas import ManifestSchema1

        Loader.__init__(self, Manifest)
        self.add_schema(ManifestSchema1, 1)
