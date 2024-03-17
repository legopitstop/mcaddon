from enum import Enum

from .exception import RegistryError
from .util import Identifier, Identifiable


class Registries(Enum):

    # Global

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
    ELEMENT_TYPE = Identifier("element_type")
    FEATURE_TYPE = Identifier("feature_type")

    TREE_TRUNK = Identifier("tree_trunk")
    TREE_CANOPY = Identifier("tree_canopy")
    TREE_ROOT = Identifier("tree_root")

    BEHAVIOR_PACK_FILE = Identifier("behavior_pack_file")
    RESOURCE_PACK_FILE = Identifier("resource_pack_file")

    # Pack Only - unimplemented

    RECIPE = Identifier("recipe")
    ITEM = Identifier("item")
    BLOCK = Identifier("block")
    FEATURE = Identifier("feature")
    FEATURE_RULE = Identifier("feature_rule")
    VOLUME = Identifier("volume")
    CAMERA = Identifier("camera")
    LOOT_TABLE = Identifier("loot_table")
    TRADING = Identifier("trading")
    ENTITY = Identifier("entity")
    ANIMATION = Identifier("animation")
    ANIMATION_CONTROLLER = Identifier("animation_controller")
    RENDER_CONTROLLER = Identifier("render_controller")
    ATTACHABLE = Identifier("attachable")
    FOG = Identifier("fog")
    MODEL = Identifier("model")
    BIOME = Identifier("biome")
    CLIENT_BIOME = Identifier("client_biome")
    PARTICLE = Identifier("particle")
    PIECE = Identifier("piece")
    SPAWN_RULE = Identifier("spawn_rule")
    STRUCTURE = Identifier("structure")
    UI = Identifier("ui")


class RegistryKey:
    def __init__(self, type):
        self.type = type
        self.instances = {}

    def __iter__(self):
        for k, v in self.instances.items():
            yield v

    def __str__(self) -> str:
        return "RegistryKey{" + str(self.type) + "}"

    def keys(self):
        return self.instances.keys()

    def values(self):
        return self.instances.values()

    def items(self):
        return self.instances.items()

    def get(self, identifier: Identifiable):
        id = Identifiable.of(identifier)
        for k, v in self.instances.items():
            if k == id:
                return v
        return None

    def register(self, identifier: Identifiable, obj):
        if not issubclass(obj, self.type):
            raise TypeError(
                f"Expected {self.type.__name__} but got '{obj.__name__}' instead"
            )
        id = Identifiable.of(identifier)
        if id in self.instances:
            raise RegistryError(f"'{identifier}' is already registered!")
        self.instances[id] = obj
        return obj


class Registry:
    def __init__(self):
        self.registries = {}

    def register(self, registry: Registries, identifier: Identifiable, obj):
        return self.get_registry(registry).register(identifier, obj)

    def get_registry(self, registry: Registries) -> RegistryKey:
        return self.registries[registry._value_]

    def create_registry(self, registry: Registries, type) -> None:
        self.registries[registry._value_] = RegistryKey(type)
        return None


INSTANCE = Registry()
