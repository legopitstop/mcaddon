from typing import Self
import re

from .constant import Category


def stringify(self, args):
    inner = ", ".join([f"{k}={repr(getattr(self, k))}" for k in args])
    return f"{self.__class__.__name__}({inner})"


def getattr2(o, name, default=None):
    """
    Normal getattr function but if not defined it uses setattr and returns the default value
    """
    res = getattr(o, name, None)
    if res is None:
        setattr(o, name, default)
        return default
    return res


# Should extend datapackutils.Identifier to include AUX values
class Identifier:
    DEFAULT_NAMESPACE = "minecraft"
    SEPERATOR = ":"

    def __init__(self, namespace: str, path: str = None):
        if path is None:
            id = Identifier.parse(namespace)
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
        other = Identifier(other)
        return self.namespace == other.namespace and self.path == other.path

    def __add__(self, other) -> str:
        if isinstance(other, Identifier):
            return str(self) + str(other)
        return str(self) + other

    def __inter__(self):
        for x in self.split():
            yield x

    def __hash__(self):
        return hash((self.namespace, self.path))

    @property
    def __dict__(self) -> dict:
        data = {"namespace": self.namespace, "path": self.path}
        return data

    @property
    def namespace(self) -> str:
        return getattr(self, "_namespace", self.DEFAULT_NAMESPACE)

    @namespace.setter
    def namespace(self, value: str | None):
        if value is None or value == "":
            setattr(self, "_namespace", self.DEFAULT_NAMESPACE)
        elif isinstance(value, Identifier):
            self.namespace = value.namespace
        elif self.is_namespace_valid(value):
            setattr(self, "_namespace", str(value).strip())
        else:
            raise ValueError(value)

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
            setattr(self, "_path", str(value).strip())
        else:
            raise ValueError(value)

    def is_path_valid(self, path: str = None) -> bool:
        """
        Validates the path

        :param path: The path to validate, defaults to self.path
        :type path: str, optional
        :return: Whether or not it's valid
        :rtype: bool
        """
        v = self.path if path is None else path
        res = re.match(r"^[a-zA-Z-0-9/_\.]+$", v)
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

    @classmethod
    def parse(cls, value: str) -> Self:
        """
        Parse this value as an identifier

        :param value: The value to parse
        :type value: str
        :rtype: Identifier
        """
        self = cls.__new__(cls)
        if isinstance(value, Identifier):
            return value.copy()

        if str(value).count(self.SEPERATOR) == 0:
            self.path = value
        else:
            x = str(value).split(self.SEPERATOR)
            self.namespace = x[0]
            self.path = x[1]
        return self

    def copy(self) -> Self:
        """
        Returns a copy of this identifier

        :rtype: Identifier
        """
        return Identifier(self.namespace, self.path)

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

    def split(self) -> tuple:
        """
        Returns (namespace, path)
        """
        return (self.namespace, self.path)

    def replace(self, old, new, count=-1) -> Self:
        self.path.replace(old, new, count)
        return self


ID = Identifier


class Identifiable:
    def __init__(self, identifier: Identifier):
        self.identifier = identifier

    @property
    def identifier(self) -> Identifier:
        """The unique identifier for this object. It must be of the form 'namespace:name', where namespace cannot be 'minecraft'."""
        return getattr(self, "_identifier")

    @identifier.setter
    def identifier(self, value: Identifier):
        if not isinstance(value, (Identifier, str)):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        id = Identifier(value)
        self.filename = id.path
        setattr(self, "_identifier", id)


class Version:
    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self) -> str:
        return ".".join([str(i) for i in self.__dict__])

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
    def __dict__(self) -> list:
        return [self.major, self.minor, self.patch]

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
        setattr(self, "_patch", value)

    @classmethod
    def parse(cls, s: str | list) -> Self:
        self = cls.__new__(cls)
        if isinstance(s, list):
            self.major = s[0]
            self.minor = s[1]
            self.patch = s[2]
        else:
            major, minor, patch = str(s).split(".")
            self.major = int(major)
            self.minor = int(minor)
            self.patch = int(patch)
        return self


class MenuCategory:
    def __init__(
        self,
        category: Category | str,
        group: str = None,
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

    @property
    def __dict__(self) -> dict:
        data = {"category": self.category._value_}
        if self.category._value_ != "none":
            data["group"] = self.group
        if self.is_hidden_in_commands:
            data["is_hidden_in_commands"] = self.is_hidden_in_commands
        return data

    @property
    def category(self) -> Category:
        return getattr(self, "_category")

    @category.setter
    def category(self, value: Category):
        if isinstance(value, Category):
            setattr(self, "_category", value)
        else:
            self.category = Category[str(value).lower()]

    @property
    def group(self) -> str:
        return getattr(self, "_group", "itemGroup.search")

    @group.setter
    def group(self, value: str):
        if value is None:
            self.group = "itemGroup.search"
            return
        setattr(self, "_group", str(value))

    @property
    def is_hidden_in_commands(self) -> bool:
        return getattr(self, "_is_hidden_in_commands")

    @is_hidden_in_commands.setter
    def is_hidden_in_commands(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_is_hidden_in_commands", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "category" in data:
            self.category = data.pop("category")
        if "group" in data:
            self.group = data.pop("group")
        if "is_hidden_in_commands" in data:
            self.is_hidden_in_commands = data.pop("is_hidden_in_commands")
        return self


class Box:
    def __init__(self, origin: list = None, size: list = None):
        self.origin = origin
        self.size = size

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.origin is not None:
            data["origin"] = self.origin
        if self.size is not None:
            data["size"] = self.size
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
    def origin(self) -> list[float]:
        """Minimal position of the bounds of the box. "origin" is specified as [x, y, z] and must be in the range (-8, 0, -8) to (8, 16, 8), inclusive, defaults to [-8.0, 0, -8.0]"""
        return getattr(self, "_origin", None)

    @origin.setter
    def origin(self, value: list[float]):
        if value is None:
            setattr(self, "_origin", [-8.0, 0, -8.0])
            return
        elif isinstance(value, bool):
            setattr(self, "_origin", value)
        elif isinstance(value, list):
            setattr(self, "_origin", value)
        else:
            raise TypeError(
                f"Expected list[float] but got '{value.__class__.__name__}' instead"
            )

    @property
    def size(self) -> list[float]:
        """Size of each side of the box. Size is specified as [x, y, z]. "origin" + "size" must be in the range (-8, 0, -8) to (8, 16, 8), inclusive, defaults to [16.0, 16.0, 16.0]"""
        return getattr(self, "_size", None)

    @size.setter
    def size(self, value: list[float]):
        if value is None:
            setattr(self, "_size", [16, 16, 16])
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list[float] but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_size", value)

    def is_cube(self) -> bool:
        return self.origin == [-8, 0, -8] and self.size == [16, 16, 16]

    def is_none(self) -> bool:
        return self.origin == [0, 0, 0] and self.size == [0, 0, 0]

    @classmethod
    def cube(cls) -> Self:
        self = cls.__new__(cls)
        self.origin = [-8, 0, -8]
        self.size = [16, 16, 16]
        return self

    @classmethod
    def none(cls) -> Self:
        self = cls.__new__(cls)
        self.origin = [0, 0, 0]
        self.size = [0, 0, 0]
        return self
