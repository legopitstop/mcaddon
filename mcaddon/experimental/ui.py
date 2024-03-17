from typing import Self

from ..registry import INSTANCE, Registries
from ..file import JsonFile
from ..util import getattr2, Identifier, Identifiable


class UIGlobalVariables(JsonFile):
    FILEPATH = "ui8/_global_variables.json"

    def __init__(self, variables: dict[str] = None):
        self.variables = variables

    def __getitem__(self, key: str):
        return self.variables.get(key)

    def __setitem__(self, key: str, value):
        self.variables[str(key)] = value

    def jsonify(self) -> dict:
        data = {}
        for k, v in self.variables.items():
            data[str(k)] = v
        return data

    @property
    def variables(self) -> dict:
        return getattr2(self, "_variables", {})

    @variables.setter
    def variables(self, value: dict):
        if value is None:
            self.variables = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_variables", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.variables = data
        return self

    def get_variable(self, key: str) -> str:
        return self.variables.get(key)

    def add_variable(self, key: str, value) -> str:
        self.variables[key] = value
        return value

    def remove_variable(self, key: str) -> str:
        return self.variables.pop(key)

    def clear_variables(self) -> Self:
        self.variables = {}
        return self

    def get(self, key: str):
        return self.variables.get(key)

    def set(self, key: str, value):
        return self.variables[key](value)


class UIDefs(JsonFile):
    FILEPATH = "ui/_ui_defs.json"

    def __init__(self, definitions: list[str] = None):
        self.definitions = definitions

    def __iter__(self):
        for i in self.definitions:
            yield i

    def jsonify(self) -> dict:
        data = {"ui_defs": [str(x) for x in self.definitions]}
        return data

    @property
    def definitions(self) -> list[str]:
        return getattr2(self, "_definitions", [])

    @definitions.setter
    def definitions(self, value: list[str]):
        if value is None:
            self.definitions = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_definitions", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "ui_defs" in data:
            self.definitions = data.pop("ui_defs")
        return self

    def get_definition(self, index: int) -> str:
        return self.definitions[index]

    def add_definition(self, fp: str) -> str:
        self.definitions.append(fp)
        return fp

    def remove_definition(self, index: int) -> str:
        return self.definitions.pop(index)

    def clear_definitions(self) -> Self:
        self.definitions = []
        return self


class Element(Identifiable):
    def __init__(self): ...

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        if not isinstance(value, Identifier):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_id", value)


INSTANCE.create_registry(Registries.ELEMENT_TYPE, Element)


def element_type(cls):
    """
    Add this element type to the registry
    """

    def wrapper():
        return INSTANCE.register(Registries.ELEMENT_TYPE, cls.id, cls)

    return wrapper()


@element_type
class LabelElement(Element):
    """
    for creating text objects
    """

    id = Identifier("label")

    def __init__(self): ...


@element_type
class ImageElement(Element):
    """
    for rendering images from a filepath provided
    """

    id = Identifier("image")

    def __init__(self): ...


@element_type
class ButtonElement(Element):
    """
    for creating interactive and clickable elements
    """

    id = Identifier("button")

    def __init__(self): ...


@element_type
class PanelElement(Element):
    """
    an empty container where you can store all other elements that may overlap to each other
    """

    id = Identifier("panel")

    def __init__(self): ...


@element_type
class StackPanelElement(Element):
    """
    an empty container where you can store all other elements in a stack that doesn't overlap to each other
    """

    id = Identifier("stack_panel")

    def __init__(self): ...


@element_type
class GridElement(Element):
    """
    uses another element as a template, and then renders it repeatedly in multiple rows and columns
    """

    id = Identifier("grid")

    def __init__(self): ...


@element_type
class FactoryElement(Element):
    """
    renders an element based off of another element, is capable of calling hardcoded values and variables
    """

    id = Identifier("factory")

    def __init__(self): ...


@element_type
class CustomElement(Element):
    """
    is paired with another property renderer which renders hardcoded JSON UI elements
    """

    id = Identifier("custom")

    def __init__(self): ...


@element_type
class ScreenElement(Element):
    """
    elements that are called by the game directly, usually root panel elements
    """

    id = Identifier("screen")

    def __init__(self): ...
