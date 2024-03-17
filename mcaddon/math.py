from typing import Self
from dataclasses import dataclass
import numpy as np


class Vector2(np.ndarray):
    def __new__(cls, x: float | int = 0, y: float | int = 0):
        obj = np.asarray([x, y]).view(cls)
        return obj

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __eq__(self, other):
        return np.array_equal(self, other)

    def __ne__(self, other):
        return not np.array_equal(self, other)

    def __iter__(self):
        for x in np.nditer(self):
            yield x.item()

    def dist(self, other):
        return np.linalg.norm(self - other)

    @staticmethod
    def of(data: list) -> Self:
        if isinstance(data, list):
            if len(data) != 2:
                raise IndexError(data)
            return Vector2(*data)
        return Vector2(*str(data).split(" "))

    @staticmethod
    def from_dict(data: dict) -> Self:
        return Vector2.of(data)

    def jsonify(self) -> dict:
        return [float(x) for x in self]


class Vector3(np.ndarray):
    def __new__(cls, x: float | int = 0, y: float | int = 0, z: float | int = 0):
        obj = np.asarray([x, y, z]).view(cls)
        return obj

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    def __eq__(self, other):
        return np.array_equal(self, other)

    def __ne__(self, other):
        return not np.array_equal(self, other)

    def __iter__(self):
        for x in np.nditer(self):
            yield x.item()

    def dist(self, other):
        return np.linalg.norm(self - other)

    @staticmethod
    def of(data: list) -> Self:
        if isinstance(data, list):
            if len(data) != 3:
                raise IndexError(data)
            return Vector3(*data)
        return Vector3(*str(data).split(" "))

    @staticmethod
    def from_dict(data: dict) -> Self:
        return Vector3.of(data)

    def jsonify(self) -> dict:
        return [float(x) for x in self]


class Range(np.ndarray):
    def __new__(cls, min: float | int = 0, max: float | int = 0):
        obj = np.asarray([min, max]).view(cls)
        return obj

    @property
    def min(self):
        return self[0]

    @property
    def max(self):
        return self[1]

    def __eq__(self, other):
        return np.array_equal(self, other)

    def __ne__(self, other):
        return not np.array_equal(self, other)

    def __iter__(self):
        for x in np.nditer(self):
            yield x.item()

    def dist(self, other):
        return np.linalg.norm(self - other)

    @staticmethod
    def of(data: list) -> Self:
        if isinstance(data, list):
            if len(data) != 2:
                raise IndexError(data)
            return Range(*data)
        return Range(*str(data).split(" "))

    @staticmethod
    def from_dict(data: dict, prefix: str = "") -> Self | int | float:
        if isinstance(data, (float, int)):
            return data
        elif isinstance(data, list):
            return Range(*data)
        else:
            min = data.pop(prefix + "min")
            max = data.pop(prefix + "max")
            return Range(min, max)

    def to_list(self) -> dict:
        return [x for x in self]

    def jsonify(self, prefix: str = "") -> dict:
        data = {}
        data[prefix + "min"] = float(self.min)
        data[prefix + "max"] = float(self.max)
        return data


class VectorRange:
    def __init__(self, min: Vector3, max: Vector3):
        self.min = min
        self.max = max

    @property
    def min(self) -> Vector3:
        return getattr(self, "_min")

    @min.setter
    def min(self, value: Vector3):
        if not isinstance(value, Vector3):
            raise TypeError(
                f"Expected Vector3i but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_min", value)

    @property
    def max(self) -> Vector3:
        return getattr(self, "_max")

    @max.setter
    def max(self, value: Vector3):
        if not isinstance(value, Vector3):
            raise TypeError(
                f"Expected Vector3i but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_max", value)

    @classmethod
    def from_dict(cls, data: dict, prefix: str = "") -> Self:
        self = cls.__new__(cls)
        self.min = Vector3.of(data.pop(prefix + "min"))
        self.max = Vector3.of(data.pop(prefix + "max"))
        return self

    def jsonify(self, prefix: str = "") -> dict:
        data = {}
        data[prefix + "min"] = self.min.jsonify()
        data[prefix + "max"] = self.max.jsonify()
        return data


class Slope(np.ndarray):
    def __new__(cls, rise: float | int = 0, run: float | int = 0):
        obj = np.asarray([rise, run]).view(cls)
        return obj

    @property
    def rise(self):
        return self[0]

    @property
    def run(self):
        return self[1]

    def __eq__(self, other):
        return np.array_equal(self, other)

    def __ne__(self, other):
        return not np.array_equal(self, other)

    def __iter__(self):
        for x in np.nditer(self):
            yield x.item()

    def dist(self, other):
        return np.linalg.norm(self - other)

    @staticmethod
    def of(data: list) -> Self:
        if isinstance(data, list):
            if len(data) != 2:
                raise IndexError(data)
            return Slope(*data)
        return Slope(*str(data).split(" "))

    @staticmethod
    def from_dict(data: dict, prefix: str = "") -> Self | int | float:
        if isinstance(data, (float, int)):
            return data
        rise = data.pop(prefix + "rise")
        run = data.pop(prefix + "run")
        return Range(rise, run)

    def to_list(self) -> dict:
        return [x for x in self]

    def jsonify(self, prefix: str = "") -> dict:
        data = {}
        data[prefix + "rise"] = float(self.rise)
        data[prefix + "run"] = float(self.run)
        return data


@dataclass
class Chance:
    numerator: float
    denominator: float

    @staticmethod
    def from_dict(data: dict) -> Self:
        return Chance(**data)

    def jsonify(self) -> dict:
        data = {"numerator": self.numerator, "denominator": self.denominator}
        return data
