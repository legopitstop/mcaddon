from typing import Self
from uuid import uuid4

from .constant import ModuleType
from .util import Saveable

MIN_ENGINE_VERSION = [1, 20, 51]
FORMAT_VERSION = 1
__all__ = ['Header','Metadata','Dependency','Module', 'Manifest']

class Header:
    def __init__(self, min_engine_version:list[int]=None, name:str='Example', description:str='Generated using mcpackutils', uuid:str=None, version:list[int]=None, allow_random_seed:bool=None, base_game_version:list[int]=None, lock_template_options:bool=None):
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
            'name': self.name_key,
            'description': self.description_key,
            'uuid': self.uuid,
            'version': self.version
        }
        if self.allow_random_seed:
            data['allow_random_seed'] = self.allow_random_seed
        if self.base_game_version:
            data['base_game_version'] = self.base_game_version
        if self.lock_template_options:
            data['lock_template_options'] = self.lock_template_options
        return data

    @property
    def name_key(self) -> str:
        return getattr(self, '_name_key', 'pack.name')
    
    @name_key.setter
    def name_key(self, value:str):
        if value is None: self.name_key = 'pack.name'
        else: setattr(self, '_name_key', str(value))

    @property
    def description_key(self) -> str:
        return getattr(self, '_description_key', 'pack.description')
    
    @description_key.setter
    def description_key(self, value:str):
        if value is None: self.description_key = 'pack.description'
        else: setattr(self, '_description_key', str(value))

    @property
    def name(self) -> str:
        return getattr(self, '_name', 'Example')
    
    @name.setter
    def name(self, value:str):
        setattr(self, '_name', str(value))

    @property
    def description(self) -> str:
        return getattr(self, '_description', 'Auto generated')
    
    @description.setter
    def description(self, value:str):
        setattr(self, '_description', str(value))

    @property
    def min_engine_version(self) -> list[int]:
        return getattr(self, '_min_engine_version', MIN_ENGINE_VERSION)
    
    @min_engine_version.setter
    def min_engine_version(self, value:list[int]):
        if value is None:
            self.min_engine_version = MIN_ENGINE_VERSION
            return
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_min_engine_version', value)

    @property
    def uuid(self) -> str:
        return getattr(self, '_uuid', uuid4())
    
    @uuid.setter
    def uuid(self, value:str):
        if value is None: self.uuid = uuid4()
        else: setattr(self, '_uuid', str(value))

    @property
    def version(self) -> list[int]:
        return getattr(self, '_version', [1,0,0])
    
    @version.setter
    def version(self, value:list[int]):
        if value is None:
            self.version = [1,0,0]
            return
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_version', value)

    @property
    def allow_random_seed(self) -> bool:
        return getattr(self, '_allow_random_seed', False)
    
    @allow_random_seed.setter
    def allow_random_seed(self, value:bool):
        if value is None:
            self.allow_random_seed = False
            return
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_allow_random_seed', value)

    @property
    def base_game_version(self) -> list[int]|None:
        return getattr(self, '_base_game_version', None)
    
    @base_game_version.setter
    def base_game_version(self, value:list[int]):
        if value is None:
            setattr(self, '_base_game_version', None)
            return
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_base_game_version', value)

    @property
    def lock_template_options(self) -> bool:
        return getattr(self, '_lock_template_options', False)
    
    @lock_template_options.setter
    def lock_template_options(self, value:bool):
        if value is None:
            self.lock_template_options = False
            return
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_lock_template_options', value)

class Metadata:
    def __init__(self, license:str, url:str):
        self.authors = []
        self.license = license
        self.url = url

    @property
    def __dict__(self) -> dict:
        data = {
            'authors': self.authors,
            'license': self.license,
            'url': self.url
        }
        return data

    @property
    def authors(self) -> list[str]:
        return getattr(self, '_authors')
    
    @authors.setter
    def authors(self, value:list[str]):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_authors', value)

    @property
    def license(self) -> str:
        return getattr(self, '_license')
    
    @license.setter
    def license(self, value:str):
        setattr(self, '_license', str(value))

    @property
    def url(self) -> str:
        return getattr(self, '_url')
    
    @url.setter
    def url(self, value:str):
        setattr(self, '_url', str(value))

    def add_author(self, name:str) -> str:
        self.authors.append(name)
        return name
    
    def get_author(self, index:int) -> str:
        return self.authors[index]
    
    def remove_author(self, index:int) -> str:
        name = self.authors[index]
        del self.authors[index]
        return name
    
    def clear_authors(self):
        self.authors = []
        return self

class Dependency:
    def __init__(self, uuid:str, version:list[int]=None):
        self.uuid = uuid
        self.version = version
    
    @property
    def __dict__(self) -> dict:
        data = {
            'uuid': self.uuid,
            'version': self.version
        }
        return data

    @property
    def uuid(self) -> str:
        return getattr(self, '_uuid')
    
    @uuid.setter
    def uuid(self, value:str):
        setattr(self, '_uuid', str(value))

    @property
    def version(self) -> list[int]:
        return getattr(self, '_version', [1,0,0])
    
    @version.setter
    def version(self, value:list[int]):
        if value is None:
            self.version = [1,0,0]
            return
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_version', value)

class Module:
    def __init__(self, type:ModuleType, uuid:str=None, version:list[int]=None, description:str=None):
        self.type = type
        self.description = description
        self.uuid = uuid
        self.version = version

    @property
    def __dict__(self) -> dict:
        data = {
            'description': self.description,
            'type': self.type._value_,
            'uuid': self.uuid,
            'version': self.version
        }
        return data

    @property
    def type(self) -> ModuleType:
        return getattr(self, '_type')
    
    @type.setter
    def type(self, value:ModuleType):
        if not isinstance(value, ModuleType): raise TypeError(f"Expected ModuleType but got '{value.__class__.__name__}' instead")
        setattr(self, '_type', value)

    @property
    def description(self) -> str:
        return getattr(self, '_description', 'pack.description')
    
    @description.setter
    def description(self, value:str):
        if value is None: self.description = 'pack.description'
        else: setattr(self, '_description', str(value))

    @property
    def uuid(self) -> str:
        return getattr(self, '_uuid', uuid4())
    
    @uuid.setter
    def uuid(self, value:str):
        if value is None: self.uuid = uuid4()
        else: setattr(self, '_uuid', str(value))

    @property
    def version(self) -> list[int]:
        return getattr(self, '_version', [1,0,0])
    
    @version.setter
    def version(self, value:list[int]):
        if value is None:
            self.version = [1,0,0]
            return
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_version', value)

class Manifest(Saveable):
    def __init__(self, header:Header, metadata:Metadata=None):
        self.format_version = FORMAT_VERSION
        self.header = header
        self.metadata = metadata
        self.dependencies = {}
        self.modules = {}
    
    @property
    def __dict__(self) -> dict:
        data = {
            'format_version': self.format_version,
            'header': self.header.__dict__,
            'dependencies': [],
            'modules': []
        }
        if self.metadata:
            data['metadata'] = self.metadata.__dict__
        
        if self.dependencies:
            for v in self.dependencies.values():
                data['dependencies'].append(v.__dict__)
        if self.modules:
            for v in self.modules.values():
                data['modules'].append(v.__dict__)
        return data
    
    @property
    def format_version(self) -> int:
        return getattr(self, '_format_version', FORMAT_VERSION)
    
    @format_version.setter
    def format_version(self, value:int):
        if value is None:
            self.format_version = FORMAT_VERSION
            return
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_format_version', value)

    @property
    def header(self) -> Header:
        return getattr(self, '_header')
    
    @header.setter
    def header(self, value:Header):
        if not isinstance(value, Header): raise TypeError(f"Expected Header but got '{value.__class__.__name__}' instead")
        setattr(self, '_header', value)

    @property
    def metadata(self) -> Metadata:
        return getattr(self, '_metadata', None)
    
    @metadata.setter
    def metadata(self, value:Metadata):
        if value is None:
            setattr(self, '_metadata', None)
            return
        if not isinstance(value, Metadata): raise TypeError(f"Expected Metadata but got '{value.__class__.__name__}' instead")
        setattr(self, '_metadata', value)

    @property
    def dependencies(self) -> dict[str, Dependency]:
        return getattr(self, '_dependencies', {})
    
    @dependencies.setter
    def dependencies(self, value:dict[str, Dependency]):
        if not isinstance(value, dict): raise TypeError(f"Expected dict but got '{value.__class__.__name__}' instead")
        setattr(self, '_dependencies', value)

    @property
    def modules(self) -> dict[str, Module]:
        return getattr(self, '_modules', {})
    
    @modules.setter
    def modules(self, value:dict[str, Module]):
        if not isinstance(value, dict): raise TypeError(f"Expected dict but got '{value.__class__.__name__}' instead")
        setattr(self, '_modules', value)

    def add_module(self, module:Module) -> Module:
        self.modules[module.uuid] = module
        return module
    
    def get_module(self, uuid:str) -> Module:
        return self.modules[uuid]
    
    def remove_module(self, uuid:str) -> Module:
        return self.modules.pop(uuid)

    def clear_modules(self) -> Self:
        self.modules = {}
        return self

    def add_dependency(self, dependency:Dependency) -> Dependency:
        self.dependencies[dependency.uuid] = dependency
        return dependency
    
    def get_dependency(self, uuid:str) -> Dependency:
        return self.dependencies[uuid]

    def remove_dependency(self, uuid:str) -> Dependency:
        return self.dependencies.pop(uuid)

    def clear_dependencies(self) -> Self:
        self.dependencies = {}
        return self

    @classmethod
    def behavior(cls) -> Self:
        self = cls.__new__(cls)
        self.modules = {}
        self.dependencies = {}
        self.header = Header()
        self.add_module(Module(ModuleType.DATA))
        return self
    
    @classmethod
    def resource(cls) -> Self:
        self = cls.__new__(cls)
        self.modules = {}
        self.dependencies = {}
        self.header = Header()
        self.add_module(Module(ModuleType.RESOURCES))
        return self
    
    @classmethod
    def world_template(cls) -> Self:
        self = cls.__new__(cls)
        self.modules = {}
        self.dependencies = {}
        self.header = Header()
        self.add_module(Module(ModuleType.WORLD_TEMPLATE))
        return self