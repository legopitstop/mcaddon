from typing import Self

from .util import getattr2, Misc


class Filter(Misc):
    def __init__(self, test: str, value: str, operator: str = "=="):
        self.test = test
        self.value = value
        self.operator = operator

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "Filter{" + self.test + self.operator + self.value + "}"

    @property
    def test(self) -> str:
        return getattr(self, "_test")

    @test.setter
    def test(self, value: str):
        setattr(self, "_test", str(value))

    @property
    def value(self) -> str:
        return getattr(self, "_value")

    @value.setter
    def value(self, value: str):
        setattr(self, "_value", str(value))

    @property
    def operator(self) -> str:
        return getattr(self, "_operator")

    @operator.setter
    def operator(self, value: str):
        setattr(self, "_operator", str(value))

    @staticmethod
    def from_dict(data: dict) -> Self:
        test = data.pop("test")
        value = data.pop("value")
        operator = data.pop("operator") if "operator" in data else "=="
        return Filter(test, value, operator)

    def jsonify(self) -> dict:
        data = {"test": self.test, "value": self.value}
        if self.operator:
            data["operator"] = self.operator
        return data


class Filters(Misc):
    def __init__(self, filters: list[Filter] = None):
        self.filters = filters

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.__class__.__name__ + "{" + "}"

    def __iter__(self):
        for f in self.filters:
            yield f

    def __len__(self) -> int:
        return len(self.filters)

    @property
    def filters(self) -> list[Filter]:
        return getattr2(self, "_filters", [])

    @filters.setter
    def filters(self, value: list[Filter]):
        if value is None:
            self.filters = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_filters", value)

    def get_filter(self, index: int) -> Filter | None:
        return self.filters.get(index)

    def add_filter(self, filter: Filter) -> Filter:
        if not isinstance(filter, (Filter, AllFilter, AnyFilter)):
            raise TypeError(
                f"Expected Filter, AnyFilters, AllFilters but got '{filter.__class__.__name__}' instead"
            )
        self.filters.append(filter)
        return filter

    def add_filters(self, *filter: Filter) -> list[Filter]:
        return [self.add_filter(f) for f in filter]

    def remove_filter(self, index: int) -> Filter:
        return self.filters.pop(index)

    def clear_filters(self) -> Self:
        self.filters.clear()
        return self

    @staticmethod
    def from_dict(data: list) -> Self:
        if isinstance(data, dict):
            return Filters([Filter.from_dict(data)])
        return Filters([Filter.from_dict(x) for x in data])

    def jsonify(self) -> list:
        return [x.jsonify() for x in self]


class AllFilter(Filters):
    @staticmethod
    def from_dict(data: list) -> Self:
        return AllFilter([Filter.from_dict(f) for f in data.pop("all_of")])

    def add_filter(self, filter: Filter) -> Filter:
        if not isinstance(filter, Filter):
            raise TypeError(
                f"Expected Filter but got '{filter.__class__.__name__}' instead"
            )
        self.filters.append(filter)
        return filter

    def jsonify(self) -> dict:
        data = {"all_of": [f.jsonify() for f in self.filters]}
        return data


class AnyFilter(Filters):
    @staticmethod
    def from_dict(data: dict) -> Self:
        return AnyFilter([Filter.from_dict(f) for f in data.pop("any_of")])

    def add_filter(self, filter: Filter) -> Filter:
        if not isinstance(filter, Filter):
            raise TypeError(
                f"Expected Filter but got '{filter.__class__.__name__}' instead"
            )
        self.filters.append(filter)
        return filter

    def jsonify(self) -> dict:
        data = {"any_of": [f.jsonify() for f in self.filters]}
        return data
