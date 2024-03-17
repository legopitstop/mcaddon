from typing import Self
from uuid import uuid4, UUID

from . import VERSION
from .constant import ModuleType, PackScope
from .file import JsonFile, Loader
from .util import getattr2, getitem, additem, removeitem, clearitems, Version, Misc


class Header(Misc):
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
        pack_scope: str = None,
    ):
        self.name = name
        self.uuid = uuid
        self.description = description
        self.version = version
        self.allow_random_seed = allow_random_seed
        self.base_game_version = base_game_version
        self.lock_template_options = lock_template_options
        self.min_engine_version = min_engine_version
        self.pack_scope = pack_scope

    def jsonify(self) -> dict:
        data = {
            "name": self.name_key,
            "description": self.description_key,
            "uuid": str(self.uuid),
            "version": self.version.jsonify(),
            "min_engine_version": self.min_engine_version.jsonify(),
        }
        if self.allow_random_seed:
            data["allow_random_seed"] = self.allow_random_seed
        if self.base_game_version:
            data["base_game_version"] = self.base_game_version.jsonify()
        if self.lock_template_options:
            data["lock_template_options"] = self.lock_template_options
        if self.pack_scope:
            data["pack_scope"] = self.pack_scope.jsonify()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.name = data.pop("name")
        self.description = data.pop("description")
        self.uuid = data.pop("uuid")
        self.version = Version.of(data.pop("version"))
        if "allow_random_seed" in data:
            self.allow_random_seed = data.pop("allow_random_seed")
        if "base_game_version" in data:
            self.base_game_version = Version.of(data.pop("base_game_version"))
        if "lock_template_options" in data:
            self.lock_template_options = data.pop("lock_template_options")
        if "min_engine_version" in data:
            self.min_engine_version = Version.of(data.pop("min_engine_version"))
        if "pack_scope" in data:
            self.pack_scope = PackScope.from_dict(data.pop("pack_scope"))
        return self

    @property
    def pack_scope(self) -> PackScope:
        return getattr(self, "_pack_scope", None)

    @pack_scope.setter
    def pack_scope(self, value: PackScope):
        if not isinstance(value, PackScope) and value is not None:
            raise TypeError(
                f"Expected PackScope but got '{value.__class__.__name__}' instead"
            )
        self.on_update("pack_scope", value)
        setattr(self, "_pack_scope", value)

    @property
    def name_key(self) -> str:
        return getattr(self, "_name_key", "pack.name")

    @name_key.setter
    def name_key(self, value: str):
        if value is None:
            self.name_key = "pack.name"
        else:
            v = str(value)
            self.on_update("name_key", v)
            setattr(self, "_name_key", v)

    @property
    def description_key(self) -> str:
        return getattr(self, "_description_key", "pack.description")

    @description_key.setter
    def description_key(self, value: str):
        if value is None:
            self.description_key = "pack.description"
        else:
            v = str(value)
            self.on_update("description_key", v)
            setattr(self, "_description_key", v)

    @property
    def name(self) -> str:
        return getattr(self, "_name", "Untitled")

    @name.setter
    def name(self, value: str):
        if value is None:
            self.name = "Untitled"
            return
        v = str(value)
        self.on_update("name", v)
        setattr(self, "_name", v)

    @property
    def description(self) -> str:
        return getattr(self, "_description", "Auto generated")

    @description.setter
    def description(self, value: str):
        if value is None:
            self.description = "Auto generated"
            return
        v = str(value)
        self.on_update("description", v)
        setattr(self, "_description", v)

    @property
    def min_engine_version(self) -> Version:
        return getattr2(
            self, "_min_engine_version", Version.of(VERSION["MIN_ENGINE_VERSION"])
        )

    @min_engine_version.setter
    def min_engine_version(self, value: Version):
        if value is None:
            self.min_engine_version = Version.of(VERSION["MIN_ENGINE_VERSION"])
            return
        if not isinstance(value, Version):
            raise TypeError(
                f"Expected Version but got '{value.__class__.__name__}' instead"
            )
        self.on_update("min_engine_version", value)
        setattr(self, "_min_engine_version", value)

    @property
    def uuid(self) -> UUID:
        return getattr(self, "_uuid", uuid4())

    @uuid.setter
    def uuid(self, value: UUID):
        if value is None:
            self.uuid = uuid4()
        elif isinstance(value, UUID):
            self.on_update("uuid", value)
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
        self.on_update("version", value)
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
        self.on_update("allow_random_seed", value)
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
        self.on_update("base_game_version", value)
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
        self.on_update("lock_template_options", value)
        setattr(self, "_lock_template_options", value)


class Metadata(Misc):
    def __init__(self, license: str, url: str):
        self.authors = []
        self.license = license
        self.url = url

    def jsonify(self) -> dict:
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
        self.on_update("authors", value)
        setattr(self, "_authors", value)

    @property
    def license(self) -> str:
        return getattr(self, "_license")

    @license.setter
    def license(self, value: str):
        v = str(value)
        self.on_update("license", v)
        setattr(self, "_license", v)

    @property
    def url(self) -> str:
        return getattr(self, "_url")

    @url.setter
    def url(self, value: str):
        v = str(value)
        self.on_update("url", v)
        setattr(self, "_url", v)

    def add_author(self, name: str) -> str:
        self.authors.append(name)
        return name

    def get_author(self, index: int) -> str:
        return self.authors[index]

    def remove_author(self, index: int) -> str:
        return self.authors.pop(index)

    def clear_authors(self):
        self.authors = []
        return self


class Dependency(Misc):
    def __init__(self, uuid: UUID, version: Version = None):
        self.uuid = uuid
        self.version = version

    def jsonify(self) -> dict:
        data = {"uuid": str(self.uuid), "version": self.version.jsonify()}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.uuid = data.pop("uuid")
        self.version = Version.of(data.pop("version"))
        return self

    @property
    def uuid(self) -> UUID:
        return getattr(self, "_uuid")

    @uuid.setter
    def uuid(self, value: UUID):
        if isinstance(value, UUID):
            self.on_update("uuid", value)
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
        self.on_update("version", value)
        setattr(self, "_version", value)


class Module(Misc):
    def __init__(
        self,
        type: ModuleType,
        uuid: str = None,
        version: Version = None,
        description: str = None,
    ):
        self.type = type
        self.description = description
        self.uuid = uuid
        self.version = version

    def jsonify(self) -> dict:
        data = {
            "description": self.description,
            "type": self.type.jsonify(),
            "uuid": str(self.uuid),
            "version": self.version.jsonify(),
        }
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.description = data.pop("description")
        self.type = ModuleType.from_dict(data.pop("type"))
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
        self.on_update("type", value)
        setattr(self, "_type", value)

    @property
    def description(self) -> str:
        return getattr(self, "_description", "pack.description")

    @description.setter
    def description(self, value: str):
        if value is None:
            self.description = "pack.description"
        else:
            v = str(value)
            self.on_update("description", v)
            setattr(self, "_description", v)

    @property
    def uuid(self) -> UUID:
        return getattr2(self, "_uuid", uuid4())

    @uuid.setter
    def uuid(self, value: UUID):
        if value is None:
            self.uuid = uuid4()
        elif isinstance(value, UUID):
            self.on_update("uuid", value)
            setattr(self, "_uuid", value)
        else:
            self.uuid = UUID(str(value))

    @property
    def version(self) -> Version:
        return getattr(self, "_version", Version(1, 0, 0))

    @version.setter
    def version(self, value: Version):
        v = Version.of(value)
        self.on_update("version", v)
        setattr(self, "_version", v)

    @classmethod
    def resources(cls, uuid: UUID = None) -> Self:
        self = cls.__new__(cls)
        self.type = ModuleType.RESOURCES
        self.uuid = uuid
        return self

    @classmethod
    def data(cls, uuid: UUID = None) -> Self:
        self = cls.__new__(cls)
        self.type = ModuleType.DATA
        self.uuid = uuid
        return self

    @classmethod
    def client_data(cls, uuid: UUID = None) -> Self:
        self = cls.__new__(cls)
        self.type = ModuleType.CLIENT_DATA
        self.uuid = uuid
        return self

    @classmethod
    def interface(cls, uuid: UUID = None) -> Self:
        self = cls.__new__(cls)
        self.type = ModuleType.INTERFACE
        self.uuid = uuid
        return self

    @classmethod
    def world_template(cls, uuid: UUID = None) -> Self:
        self = cls.__new__(cls)
        self.type = ModuleType.WORLD_TEMPLATE
        self.uuid = uuid
        return self


class Manifest(JsonFile):
    """
    Represents a Pack Manifest.
    """

    FILEPATH = "manifest.json"

    def __init__(
        self,
        header: Header,
        metadata: Metadata = None,
        dependencies: dict[str, Dependency] = {},
        modules: dict[str, Module] = {},
    ):
        self.header = header
        self.metadata = metadata
        self.dependencies = dependencies
        self.modules = modules

    def __iter__(self):
        for i in self.modules:
            yield i

    def __str__(self):
        return "Manifest{" + str(self.header.uuid) + "}"

    def jsonify(self) -> dict:
        data = {
            "format_version": VERSION["MANIFEST"],
            "header": self.header.jsonify(),
            "modules": [],
        }

        if self.metadata:
            data["metadata"] = self.metadata.jsonify()

        if self.dependencies:
            data["dependencies"] = []
            for v in self.dependencies.values():
                data["dependencies"].append(v.jsonify())
        if self.modules:
            for v in self.modules.values():
                data["modules"].append(v.jsonify())
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
        self.FILEFILEPATH = value.name
        self.on_update("header", value)
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
        self.on_update("metadata", value)
        setattr(self, "_metadata", value)

    @property
    def dependencies(self) -> dict[str, Dependency]:
        return getattr2(self, "_dependencies", {})

    @dependencies.setter
    def dependencies(self, value: dict[str, Dependency]):
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        self.on_update("dependencies", value)
        setattr(self, "_dependencies", value)

    @property
    def modules(self) -> dict[str, Module]:
        return getattr2(self, "_modules", {})

    @modules.setter
    def modules(self, value: dict[str, Module]):
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        self.on_update("modules", value)
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

    def get_module(self, uuid: UUID) -> Module:
        return getitem(self, "modules", uuid)

    def add_module(self, module: Module) -> Module:
        return additem(self, "modules", module, module.uuid, Module)

    def set_module(self, module: Module) -> Module:
        self.clear_modules()
        return self.add_module(module)

    def remove_module(self, uuid: UUID) -> Module:
        return removeitem(self, "modules", uuid)

    def clear_modules(self) -> Self:
        return clearitems(self, "modules")

    def get_dependency(self, uuid: UUID) -> Dependency:
        return getitem(self, "dependencies", uuid)

    def add_dependency(self, obj: Dependency | Self) -> Dependency:
        from .pack import Pack

        if isinstance(obj, Manifest):
            return self.add_dependency(Dependency(obj.header.uuid, obj.header.version))
        elif isinstance(obj, Pack):
            return self.add_dependency(
                Dependency(obj.manifest.header.uuid, obj.manifest.header.version)
            )
        return additem(self, "dependencies", obj, obj.uuid, Dependency)

    def remove_dependency(self, uuid: UUID) -> Dependency:
        return removeitem(self, "dependencies", uuid)

    def clear_dependencies(self) -> Self:
        """Remove all dependencies"""
        return clearitems(self, "dependencies")

    def set_uuids(self, header_uuid: str, *module_uuid: str) -> Self:
        self.header.uuid = header_uuid
        for idx, uuid in enumerate(module_uuid):
            m = list(self.modules.values())[idx]
            m.uuid = uuid
        return self

    def has_behavior(self) -> bool:
        return ModuleType.DATA in [m.type for m in self.modules.values()]

    def has_resource(self) -> bool:
        return ModuleType.RESOURCES in [m.type for m in self.modules.values()]

    def has_world_template(self) -> bool:
        return ModuleType.WORLD_TEMPLATE in [m.type for m in self.modules.values()]

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
        self.add_schema(ManifestSchema1, 2)
