from typing import Self
from .util import Identifier

# __all__ = ['Entity']

class EntityComponent:
    @classmethod
    def from_dict(cls, data:dict) -> Self:
        raise NotImplementedError()

COMPONENTS:dict[str, EntityComponent] = {}
def component(cls):
    def wrapper():
        global COMPONENTS
        COMPONENTS[cls.id] = cls
        return cls
    return wrapper()


class Entity:
    format_version = '1.20.51'
    id = Identifier('entity')
