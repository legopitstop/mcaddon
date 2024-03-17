from typing import Self, Callable, Any
import re
import os

from .constant import Category, ItemGroup
from .math import Vector3


def stringify(self, args):
    inner = ", ".join([f"{k}={repr(getattr(self, k))}" for k in args])
    return f"{self.__class__.__name__}({inner})"


def splitpath(path: str) -> tuple[str, str, str]:
    """
    Splits the path into 3 parts. `root/dirname/filename.extension` -> (`root/dirname`, `filename`, `.extension`)

    :param path: The path to split
    :type path: str
    :return: 3 parts of the path (dirname, filename, extension)
    :rtype: tuple[str, str, str]
    """
    a = os.path.dirname(path)
    b, c = os.path.splitext(os.path.basename(path))
    return a, b, c


def modpath(path: str, part: str, value: str) -> str:
    """
    Modify a part of a path.

    :param path: The main path to modify.
    :type path: str
    :param part: The part to modify. `d` - dirname. `f` - filename. `e` - extension.
    :type part: str
    :param value: The value to place
    :type value: str
    :return: The modified path.
    :rtype: str
    """
    a, b, c = splitpath(path)
    if value == "" or value is None:
        return path
    match part.lower():
        case "d":
            return os.path.join(value, b + c)
        case "f":
            return os.path.join(a, value + c)
        case "e":
            return os.path.join(a, b + value)
    return path


# Rename to getsetattr
def getattr2(obj, name, default=None):
    """
    Normal getattr function but if not defined it uses setattr and returns the default value
    """
    res = getattr(obj, name, None)
    if res is None:
        setattr(obj, name, default)
        return default
    return res


def setattr2(obj, name: str, value, type=None):
    """
    setattr method but has type checking and list/dict defaults.
    """
    if value is None:
        if issubclass(type, list):
            value = []
        if issubclass(type, dict):
            value = {}
    if type is not None and not isinstance(value, type):
        raise TypeError(
            f"Expected {type.__class__.__name__} but got '{value.__class__.__name__}' instead"
        )
    setattr(obj, name, value)


def clearitems(obj, name: str):
    getattr(obj, name).clear()
    return obj


def removeitem(obj, name: str, key: Any):
    return getattr(obj, name).pop(key)


def getitem(obj, name: str, key: Any):
    return getattr(obj, name)[key]


def additem(obj, name: str, value: Any, key: Any = None, type=None):
    v = getattr(obj, name)
    if type is not None and not isinstance(value, type):
        raise TypeError(
            f"Expected {type.__class__.__name__} but got '{value.__class__.__name__}' instead"
        )
    if key is None:
        v.append(value)
    else:
        v[key] = value
    return value


class Misc:
    _events = {}

    def on_update(self, name: str, value: Any):
        if name in self._events:
            for func in self._events[name]:
                self._events[name](value)

    def bind(self, name: str, func: Callable) -> Self:
        if name not in self._events:
            self._events[name] = []
        self._events[name].append(func)
        return self

    def copy(self) -> Self:
        return self.from_dict(self.jsonify())


# Should extend datapackutils.Identifier to include AUX values
class Identifier(Misc):
    """Represents a string which contains a `namespace` and `path`"""

    DEFAULT_NAMESPACE = "minecraft"
    SEPERATOR = ":"

    def __init__(self, namespace: str, path: str = None):
        if path is None:
            id = Identifier.of(namespace)
            self.namespace = id.namespace
            self.path = id.path
        else:
            self.namespace = namespace
            self.path = path

    def __repr__(self) -> str:
        return repr(str(self))

    def __str__(self) -> str:
        return (
            self.namespace
            if self.path is None
            else self.namespace + str(self.SEPERATOR) + self.path
        )

    def __eq__(self, other) -> bool:
        other = Identifiable.of(other)
        return self.namespace == other.namespace and self.path == other.path

    def __add__(self, other) -> str:
        if isinstance(other, Identifier):
            return str(self) + str(other)
        return str(self) + other

    def __len__(self) -> int:
        return len(str(self))

    def __inter__(self):
        for x in self.split():
            yield x

    def __hash__(self):
        return hash((self.namespace, self.path))

    @property
    def namespace(self) -> str:
        return getattr(self, "_namespace", self.DEFAULT_NAMESPACE)

    @namespace.setter
    def namespace(self, value: str | None):
        if value is None or value == "" or value.lower() == "none":
            self.namespace = self.DEFAULT_NAMESPACE
        elif isinstance(value, Identifier):
            self.namespace = value.namespace
        elif self.is_namespace_valid(value):
            v = str(value).strip()
            self.on_update("namespace", v)
            setattr(self, "_namespace", v)
        else:
            raise ValueError(repr(value))

    @property
    def path(self) -> str | None:
        return getattr(self, "_path", "air")

    @path.setter
    def path(self, value: str):
        if value is None or value == "":
            setattr(self, "_path", None)
        elif isinstance(value, Identifier):
            self.path = value.path
        elif self.is_path_valid(str(value)):
            v = str(value).strip()
            self.on_update("path", v)
            setattr(self, "_path", v)
        else:
            raise ValueError(value)

    # Read-Only
    @property
    def identifier(self) -> Self:
        return self

    @staticmethod
    def from_dict(data: dict) -> Self:
        return Identifier(**data)

    @staticmethod
    def of(value: str) -> Self:
        """
        Parse this value as an identifier

        :param value: The value to parse
        :type value: str
        :rtype: Identifier
        """
        if isinstance(value, Identifier):
            return value.copy()

        if str(value).count(Identifier.SEPERATOR) == 0:
            return Identifier(Identifier.DEFAULT_NAMESPACE, value)
        return Identifier(*str(value).split(Identifier.SEPERATOR, 1))

    def jsonify(self) -> dict:
        data = {"namespace": self.namespace, "path": self.path}
        return data

    def is_path_valid(self, path: str = None) -> bool:
        """
        Validates the path

        :param path: The path to validate, defaults to self.path
        :type path: str, optional
        :return: Whether or not it's valid
        :rtype: bool
        """
        v = self.path if path is None else path
        res = re.match(r"^[a-zA-Z-0-9/_\.:]+$", v)
        return res is not None

    def is_namespace_valid(self, namespace: str = None) -> bool:
        """
        Validates the namespace

        :param namespace: The namespace to validate, defaults to self.namespace
        :type namespace: str, optional
        :return: Whether or not it's valid
        :rtype: bool
        """
        v = self.namespace if namespace is None else namespace
        res = re.match(r"^[a-z0-9_]+$", v)
        return res is not None

    def copy_with_path(self, path: str) -> Self:
        """
        Returns a copy of this identifier with a new path

        :rtype: Identifier
        """
        id = self.copy()
        id.path = path.path if isinstance(path, Identifier) else path
        return id

    def copy_with_namespace(self, namespace: str) -> Self:
        """
        Returns a copy of this identifier with a new namespace

        :rtype: Identifier
        """
        id = self.copy()
        id.namespace = (
            namespace.namespace if isinstance(namespace, Identifier) else namespace
        )
        return id

    def split(self) -> tuple[str, str]:
        """
        Returns the Identifier split as (namespace, path)

        :rtype: tuple[str, str]
        """
        return (self.namespace, self.path)

    def replace(self, old: str, new: str, count=-1) -> Self:
        """
        Replace text in path

        :param old: The text to replace
        :type old: str
        :param new: The new text to replace with
        :type new: str
        :param count: Maximum number of occurrences to replace., defaults to -1
        :type count: int, optional
        :rtype: Identifier
        """
        self.path.replace(old, new, count)
        return self

    def suffix(self, suffix: str) -> Self:
        """
        Add suffix to the end of the path

        :param suffix: The path suffix
        :type suffix: str
        :rtype: Identifier
        """
        self.path += str(suffix)
        return self

    def prefix(self, prefix) -> Self:
        """
        Add prefix to the start of the path

        :param prefix: The path prefix
        :rtype: Identifier
        """
        self.path = str(prefix) + self.path
        return self


ID = Identifier


class Identifiable(Misc):
    def __init__(self, identifier: Identifier):
        self.identifier = identifier

    def __repr__(self) -> str:
        return self.__class__.__name__ + "{" + str(self.identifier) + "}"

    def __str__(self) -> str:
        return str(self.identifier)

    @property
    def identifier(self) -> Identifier:
        """The unique identifier for this object. It must be of the form 'namespace:name', where namespace cannot be 'minecraft'."""
        return getattr(self, "_identifier")

    @identifier.setter
    def identifier(self, value: Identifier):
        id = Identifiable.of(value)
        self.filename = id.path
        self.on_update("identifier", id)
        setattr(self, "_identifier", id)

    @staticmethod
    def of(value: str | Identifier) -> Identifier:
        if value is None:
            return Identifier("empty")
        if isinstance(value, Identifiable):
            return value.identifier
        if isinstance(value, Identifier):
            return value
        return Identifier.of(value)

    def copy_with_path(self, path: str) -> Self:
        """
        Returns a copy of this object with a new path

        :rtype: Identifiable
        """
        obj = self.copy()
        obj.identifier = obj.identifier.copy_with_path(path)
        return obj

    def copy_with_namespace(self, namespace: str) -> Self:
        """
        Returns a copy of this object with a new namespace

        :rtype: Identifiable
        """
        obj = self.copy()
        obj.identifier = obj.identifier.copy_with_namespace(namespace)
        return obj

    def copy_with(self, identifier) -> Self:
        """
        Returns a copy of this object with a new identifier

        :rtype: Identifiable
        """
        obj = self.copy()
        obj.identifier = Identifiable.of(identifier)
        return obj


class Version(Misc):
    def __init__(self, major: int, minor: int = None, patch: int = None):
        if minor == None and patch == None:
            self.major, self.minor, self.patch = Version.of(major).split()
        else:
            self.major = major
            self.minor = minor
            self.patch = patch

    def __str__(self) -> str:
        return ".".join([str(i) for i in self.jsonify()])

    def __iter__(self):
        for i in [self.major, self.minor, self.patch]:
            yield i

    def __getitem__(self, k):
        match k:
            case 0 | "0" | "major":
                return self.major
            case 1 | "1" | "minor":
                return self.minor
            case 2 | "2" | "patch":
                return self.patch
        raise KeyError(k)

    @property
    def major(self) -> int:
        return getattr(self, "_major", 0)

    @major.setter
    def major(self, value: int):
        if value is None:
            self.major = 0
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("major", value)
        setattr(self, "_major", value)

    @property
    def minor(self) -> int:
        return getattr(self, "_minor", 0)

    @minor.setter
    def minor(self, value: int):
        if value is None:
            self.minor = 0
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("minor", value)
        setattr(self, "_minor", value)

    @property
    def patch(self) -> int:
        return getattr(self, "_patch", 0)

    @patch.setter
    def patch(self, value: int):
        if value is None:
            self.patch = 0
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("patch", value)
        setattr(self, "_patch", value)

    @staticmethod
    def of(value: str | list) -> Self:
        if isinstance(value, list):
            return Version(*value)
        return Version(*str(value).split("."))

    def jsonify(self) -> list:
        return [self.major, self.minor, self.patch]

    def split(self) -> tuple:
        """
        Returns (major, minor, patch)
        """
        return (self.major, self.minor, self.patch)

    def copy(self) -> Self:
        return Version(self.major, self.minor, self.patch)


class MenuCategory(Misc):
    def __init__(
        self,
        category: Category | str,
        group: ItemGroup = ItemGroup.SEARCH,
        is_hidden_in_commands: bool = False,
    ):
        """
        The creative group name and category for this block/item

        :param category: The Creative Category that this item belongs to
        :type category: Category | str
        :param group: The Creative Group that this item belongs to. Group name is limited to 256 characters, defaults to None
        :type group: str, optional
        :param is_hidden_in_commands: Determines whether or not this item can be used with commands, defaults to False
        :type is_hidden_in_commands: bool, optional
        """
        self.category = category
        self.group = group
        self.is_hidden_in_commands = is_hidden_in_commands

    def jsonify(self) -> dict:
        data = {"category": self.category.jsonify()}
        if self.category != Category.NONE:
            data["group"] = self.group.jsonify()
        if self.is_hidden_in_commands:
            data["is_hidden_in_commands"] = self.is_hidden_in_commands
        return data

    @property
    def category(self) -> Category:
        return getattr(self, "_category")

    @category.setter
    def category(self, value:Category):
        if not isinstance(value, Category): raise TypeError(f"Expected Category but got '{value.__class__.__name__}' instead")
        self.on_update("category", value)
        setattr(self, "_category", value)

    @property
    def group(self) -> ItemGroup:
        return getattr(self, "_group", ItemGroup.SEARCH)

    @group.setter
    def group(self, value: ItemGroup | None):
        if value is None:
            self.group = ItemGroup.SEARCH
            return
        if isinstance(value, ItemGroup):
            self.on_update("group", value)
            setattr(self, "_group", value)
        else:
            self.category = ItemGroup.from_dict(str(value))

    @property
    def is_hidden_in_commands(self) -> bool:
        return getattr(self, "_is_hidden_in_commands")

    @is_hidden_in_commands.setter
    def is_hidden_in_commands(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("is_hidden_in_commands", value)
        setattr(self, "_is_hidden_in_commands", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "category" in data:
            self.category = Category.from_dict(data.pop("category"))
        if "group" in data:
            self.group = ItemGroup.from_dict(data.pop("group"))
        if "is_hidden_in_commands" in data:
            self.is_hidden_in_commands = data.pop("is_hidden_in_commands")
        return self

    @staticmethod
    def none() -> Self:
        return MenuCategory(Category.NONE)

    def copy(self) -> Self:
        return MenuCategory(self.category, self.group)


class Box(Misc):
    def __init__(
        self, origin: Vector3 = Vector3(-8, 0, -8), size: Vector3 = Vector3(16, 16, 16)
    ):
        self.origin = origin
        self.size = size

    def as_dict(self) -> dict:
        data = {}
        if self.origin is not None:
            data["origin"] = self.origin.jsonify()
        if self.size is not None:
            data["size"] = self.size.jsonify()
        if isinstance(self.origin, bool):
            data = self.origin
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "origin" in data:
            self.origin = data.pop("origin")
        if "size" in data:
            self.size = data.pop("size")
        return self

    @property
    def origin(self) -> Vector3:
        """Minimal position of the bounds of the box. "origin" is specified as [x, y, z] and must be in the range (-8, 0, -8) to (8, 16, 8), inclusive, defaults to [-8.0, 0, -8.0]"""
        return getattr(self, "_origin", Vector3(-8, 0, -8))

    @origin.setter
    def origin(self, value: Vector3):
        if isinstance(value, bool):
            setattr(self, "_origin", value)
        elif isinstance(value, Vector3):
            self.on_update("origin", value)
            setattr(self, "_origin", value)
        else:
            raise TypeError(
                f"Expected Vector3 but got '{value.__class__.__name__}' instead"
            )

    @property
    def size(self) -> Vector3:
        """Size of each side of the box. Size is specified as [x, y, z]. "origin" + "size" must be in the range (-8, 0, -8) to (8, 16, 8), inclusive, defaults to [16.0, 16.0, 16.0]"""
        return getattr(self, "_size", Vector3(16, 16, 16))

    @size.setter
    def size(self, value: Vector3):
        if not isinstance(value, Vector3):
            raise TypeError(
                f"Expected list[float] but got '{value.__class__.__name__}' instead"
            )
        self.on_update("size", value)
        setattr(self, "_size", value)

    def is_cube(self) -> bool:
        return self.origin == Vector3(-8, 0, -8) and self.size == Vector3(16, 16, 16)

    def is_none(self) -> bool:
        return self.origin == Vector3(0, 0, 0) and self.size == Vector3(0, 0, 0)

    @classmethod
    def cube(cls) -> Self:
        self = cls.__new__(cls)
        self.origin = Vector3(-8, 0, -8)
        self.size = Vector3(16, 16, 16)
        return self

    @classmethod
    def none(cls) -> Self:
        self = cls.__new__(cls)
        self.origin = Vector3(0, 0, 0)
        self.size = Vector3(0, 0, 0)
        return self
