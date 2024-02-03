from enum import Enum

from .exception import RegistryError
from .util import Identifier


class Registries(Enum):
    BLOCK_COMPONENT_TYPE = Identifier("block_component_type")
    BLOCK_TYPE = Identifier("block_type")
    ITEM_COMPONENT_TYPE = Identifier("item_component_type")
    VOLUME_COMPONENT_TYPE = Identifier("volume_component_type")
    EVENT_TYPE = Identifier("event_type")
    RECIPE_TYPE = Identifier("recipe_type")
    BLOCK_TRAIT = Identifier("block_trait")
    BLOCK_STATE = Identifier("block_state")
    POOL_ENTRY_TYPE = Identifier("pool_entry_type")
    LOOT_FUNCTION_TYPE = Identifier("loot_function_type")
    LOOT_CONDITION_TYPE = Identifier("loot_condition_type")


class RegistryKey:
    def __init__(self, type):
        self.type = type
        self.instances = {}

    def __iter__(self):
        for k, v in self.instances.items():
            yield v

    def keys(self):
        return self.instances.keys()

    def values(self):
        return self.instances.values()

    def items(self):
        return self.instances.items()

    def get(self, identifier: Identifier):
        for k, v in self.instances.items():
            if k == identifier:
                return v
        return None

    def register(self, identifier: Identifier, obj):
        if not issubclass(obj, self.type):
            raise TypeError(
                f"Expected {self.type.__name__} but got '{obj.__name__}' instead"
            )
        if identifier in self.instances:
            raise RegistryError(f"'{identifier}' is already registered!")
        self.instances[identifier] = obj
        return obj


class Registry:
    def __init__(self):
        self.registryistries = {}

    def register(self, registry: Registries, identifier: Identifier, obj):
        return self.get_registry(registry).register(identifier, obj)

    def get_registry(self, registry: Registries) -> RegistryKey:
        return self.registryistries[registry._value_]

    def create_registry(self, registry: Registries, type) -> None:
        self.registryistries[registry._value_] = RegistryKey(type)
        return None


INSTANCE = Registry()
