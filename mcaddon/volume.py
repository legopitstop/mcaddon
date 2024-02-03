from typing import Self
import json

from . import VERSION
from .registry import INSTANCE, Registries
from .event import Trigger, Event
from .file import JsonFile, Loader
from .util import getattr2, Identifier, Identifiable


class VolumeComponent:
    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return "VolumeComponent{" + str(self.id) + "}"

    @property
    def __dict__(self) -> dict:
        raise NotImplementedError()

    def json(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        raise NotImplementedError()


INSTANCE.create_registry(Registries.VOLUME_COMPONENT_TYPE, VolumeComponent)


def volume_component_type(cls):
    """Add this volume component to the registry"""

    def wrapper():
        if not issubclass(cls, VolumeComponent):
            raise TypeError(
                f"Expected VolumeComponent but got '{cls.__name__}' instead"
            )
        return INSTANCE.register(Registries.VOLUME_COMPONENT_TYPE, cls.id, cls)

    return wrapper()


@volume_component_type
class FogComponent(VolumeComponent):
    """Displays the given fog whenever a player enters the volume. Each volume can only have one fog attached."""

    id = Identifier("fog")

    def __init__(self, fog_identifier: Identifier, priority: int):
        self.fog_identifier = fog_identifier
        self.priority = priority

    @property
    def __dict__(self) -> dict:
        data = {"fog_identifier": str(self.fog_identifier), "priority": self.priority}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.fog_identifier = Identifier(data.pop("fog_identifier"))
        self.priority = data.pop("priority")
        return self

    @property
    def fog_identifier(self) -> Identifier:
        """The identifier of a fog definition. Note that you will not receive any feedback if the definition does not exist."""
        return getattr(self, "_fog_identifier")

    @fog_identifier.setter
    def fog_identifier(self, value: Identifier | str):
        setattr(self, "_fog_identifier", Identifier(value))

    @property
    def priority(self) -> int:
        """The priority for this fog definition setting. Smaller numbers have higher priority. Fogs with equal priority will be combined together."""
        return getattr(self, "_priority")

    @priority.setter
    def priority(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_priority", value)


@volume_component_type
class OnActorEnterComponent(VolumeComponent):
    """Component that defines what happens when an actor enters the volume. Can contain multiple json objects."""

    id = Identifier("on_actor_enter")

    def __init__(self, on_enter: list[Trigger] = None):
        self.on_enter = on_enter

    @property
    def __dict__(self) -> dict:
        data = {"on_enter": [x.__dict__ for x in self.on_enter]}
        return data

    @property
    def on_enter(self) -> list[Trigger]:
        """Required array that contains all the triggers."""
        return getattr2(self, "_on_enter", [])

    @on_enter.setter
    def on_enter(self, value: list[Trigger]):
        if value is None:
            self.on_enter = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_on_enter", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.on_enter = [Trigger.from_dict(e) for e in data.pop("on_enter")]
        return self

    def get_event(self, index: int) -> Trigger:
        return self.on_enter[index]

    def add_event(self, event: Trigger) -> Trigger:
        self.on_enter.append(event)
        return event

    def remove_event(self, index: int) -> Trigger:
        return self.on_enter.pop(index)

    def clear_events(self) -> Self:
        self.on_enter = []
        return self


@volume_component_type
class OnActorLeaveComponent(VolumeComponent):
    """Component that defines what happens when an actor leaves the volume."""

    id = Identifier("on_actor_leave")

    def __init__(self, on_leave: list[Trigger]):
        self.on_leave = on_leave

    @property
    def __dict__(self) -> dict:
        data = {"on_leave": [x.__dict__ for x in self.on_leave]}
        return data

    @property
    def on_leave(self) -> list[Trigger]:
        """Required array that contains all the triggers."""
        return getattr2(self, "_on_leave", [])

    @on_leave.setter
    def on_leave(self, value: list[Trigger]):
        if value is None:
            self.on_leave = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_on_leave", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.on_leave = [Trigger.from_dict(e) for e in data.pop("on_leave")]
        return self

    def get_event(self, index: int) -> Trigger:
        return self.on_leave[index]

    def add_event(self, event: Trigger) -> Trigger:
        self.on_leave.append(event)
        return event

    def remove_event(self, index: int) -> Trigger:
        return self.on_leave.pop(index)

    def clear_events(self) -> Self:
        self.on_leave = []
        return self


class Volume(JsonFile, Identifiable):
    """
    Represents a Volume.
    """

    id = Identifier("volume")
    EXTENSION = ".json"
    FILENAME = "volume"
    DIRNAME = "volumes"

    def __init__(
        self,
        identifier: Identifier | str,
        components: dict[str, VolumeComponent] = None,
    ):
        Identifiable.__init__(self, identifier)
        self.components = components

    def __str__(self) -> str:
        return "Volume{" + str(self.identifier) + "}"

    @property
    def __dict__(self) -> dict:
        volume = {"description": {"identifier": str(self.identifier)}}
        if self.components:
            volume["components"] = {}
            for k, v in self.components.items():
                volume["components"][str(k)] = v.__dict__

        if self.events:
            volume["events"] = {}
            for key, events in self.events.items():
                d = {}
                for k, v in events.items():
                    d[k.path] = v.__dict__
                volume["events"][str(key)] = d

        data = {"format_version": VERSION["VOLUME"], str(self.id): volume}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = VolumeLoader()
        loader.validate(data)
        return loader.load(data)

    @property
    def components(self) -> dict[str, VolumeComponent]:
        """List of all components that used in this volume, defaults to None"""
        return getattr2(self, "_components", {})

    @components.setter
    def components(self, value: dict[str, VolumeComponent]):
        if value is None:
            self.components = {}
            return
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_components", value)

    @property
    def events(self) -> dict[Identifier, Event]:
        """List of all events that used in this volume, defaults to None"""
        return getattr2(self, "_events", {})

    @events.setter
    def events(self, value: dict[Identifier, Event]):
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_events", value)

    # COMPONENT

    def add_component(self, component: VolumeComponent) -> VolumeComponent:
        if not isinstance(component, VolumeComponent):
            raise TypeError(
                f"Expected VolumeComponent but got '{component.__class__.__name__}' instead"
            )
        self.components[component.id] = component
        return component

    def get_component(self, id: str) -> VolumeComponent:
        x = id.id if isinstance(id, VolumeComponent) else id
        return self.components.get(x)

    def remove_component(self, id: str) -> VolumeComponent:
        x = id.id if isinstance(id, VolumeComponent) else id
        return self.components.pop(x)

    def clear_components(self) -> Self:
        self.components.clear()
        return self

    # EVENT

    def add_event(self, id: Identifier | str, event: Event) -> Event:
        if not isinstance(event, Event):
            raise TypeError(
                f"Expected Event but got '{event.__class__.__name__}' instead"
            )
        i = Identifier.parse(id)
        if i in self.events:
            self.events[i][event.id] = event
            return event
        obj = {}
        obj[event.id] = event
        self.events[i] = obj
        event.id
        return event

    def get_event(self, id: Identifier | str) -> Event:
        i = Identifier.parse(id)
        return self.events.get(i)

    def remove_event(self, id: Identifier | str) -> Event:
        i = Identifier.parse(id)
        return self.events.pop(i)

    def clear_events(self) -> Self:
        self.events.clear()
        return self


class VolumeLoader(Loader):
    def __init__(self):
        from .schemas import VolumeSchema1

        Loader.__init__(self, Volume)
        self.add_schema(VolumeSchema1, "1.20.50")
