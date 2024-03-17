from typing import Self
import json

from . import VERSION
from .pack import behavior_pack
from .registry import INSTANCE, Registries
from .event import Trigger, Event
from .file import JsonFile, Loader
from .util import (
    getattr2,
    getitem,
    additem,
    removeitem,
    clearitems,
    Identifier,
    Identifiable,
    Misc,
)


class VolumeComponent(Misc):
    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return "VolumeComponent{" + str(self.id) + "}"

    def __call__(self, ctx) -> int:
        return self.execute(ctx)

    def jsonify(self) -> dict:
        raise NotImplementedError()

    def json(self) -> str:
        return json.dumps(self.jsonify())

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        raise NotImplementedError()

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    def execute(self, ctx) -> int:
        return 0

    def generate(self, ctx) -> None:
        """
        Called when this component is added to Volume or BehaviorPack

        :type ctx: Volume | BehaviorPack
        """
        ...


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

    def __init__(self, fog_identifier: Identifiable, priority: int):
        self.fog_identifier = fog_identifier
        self.priority = priority

    def jsonify(self) -> dict:
        data = {"fog_identifier": str(self.fog_identifier), "priority": self.priority}
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.fog_identifier = data.pop("fog_identifier")
        self.priority = data.pop("priority")
        return self

    @property
    def fog_identifier(self) -> Identifier:
        """The identifier of a fog definition. Note that you will not receive any feedback if the definition does not exist."""
        return getattr(self, "_fog_identifier")

    @fog_identifier.setter
    def fog_identifier(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("fog_identifier", id)
        setattr(self, "_fog_identifier", id)

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
        self.on_update("priority", value)
        setattr(self, "_priority", value)


@volume_component_type
class OnActorEnterComponent(VolumeComponent):
    """Component that defines what happens when an actor enters the volume. Can contain multiple json objects."""

    id = Identifier("on_actor_enter")

    def __init__(self, on_enter: list[Trigger] = None):
        self.on_enter = on_enter

    def jsonify(self) -> dict:
        data = {"on_enter": [x.jsonify() for x in self.on_enter]}
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
        self.on_update("on_enter", value)
        setattr(self, "_on_enter", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.on_enter = [Trigger.from_dict(e) for e in data.pop("on_enter")]
        return self

    def get_event(self, index: int) -> Trigger:
        return getitem(self, "on_enter", index)

    def add_event(self, event: Trigger) -> Trigger:
        return additem(self, "on_enter", event, type=Trigger)

    def remove_event(self, index: int) -> Trigger:
        return removeitem(self, "on_enter", index)

    def clear_events(self) -> Self:
        """Removes all on enter triggers"""
        return clearitems(self, "on_enter")


@volume_component_type
class OnActorLeaveComponent(VolumeComponent):
    """Component that defines what happens when an actor leaves the volume."""

    id = Identifier("on_actor_leave")

    def __init__(self, on_leave: list[Trigger]):
        self.on_leave = on_leave

    def jsonify(self) -> dict:
        data = {"on_leave": [x.jsonify() for x in self.on_leave]}
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
        self.on_update("on_leave", value)
        setattr(self, "_on_leave", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.on_leave = [Trigger.from_dict(e) for e in data.pop("on_leave")]
        return self

    def get_event(self, index: int) -> Trigger:
        return getitem(self, "on_leave", index)

    def add_event(self, event: Trigger) -> Trigger:
        return additem(self, "on_leave", event, type=Trigger)

    def remove_event(self, index: int) -> Trigger:
        return removeitem(self, "on_leave", index)

    def clear_events(self) -> Self:
        """Remove all on leave triggers"""
        return clearitems(self, "on_leave")


@behavior_pack
class Volume(JsonFile, Identifiable):
    """
    Represents a data-driven [Volume](https://bedrock.dev/docs/stable/Volumes).
    """

    id = Identifier("volume")
    FILEPATH = "volumes/volume.json"

    def __init__(
        self,
        identifier: Identifiable,
        components: dict[str, VolumeComponent] = None,
    ):
        Identifiable.__init__(self, identifier)
        self.components = components

    def __str__(self) -> str:
        return "Volume{" + str(self.identifier) + "}"

    def jsonify(self) -> dict:
        volume = {"description": {"identifier": str(self.identifier)}}
        if self.components:
            volume["components"] = {}
            for k, v in self.components.items():
                volume["components"][str(k)] = v.jsonify()

        if self.events:
            volume["events"] = {}
            for key, events in self.events.items():
                d = {}
                for k, v in events.items():
                    d[k.path] = v.jsonify()
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
        self.on_update("components", value)
        setattr(self, "_components", value)

    @property
    def events(self) -> dict[Identifier, Event]:
        """List of all events that used in this volume, defaults to None"""
        return getattr2(self, "_events", {})

    @events.setter
    def events(self, value: dict[Identifiable, Event]):
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        events = {}
        for k, v in value.items():
            events[Identifiable.of(k)] = v
        self.on_update("events", events)
        setattr(self, "_events", events)

    def generate(self, ctx) -> None:
        """
        Called when this item is added to ResourcePack or BehaviorPack

        :type ctx: ResourcePack | BehaviorPack
        """
        for c in self.components.values():
            c.generate(ctx)
        for e in self.events.values():
            e.generate(ctx)

    # COMPONENT

    def get_component(self, id: Identifiable) -> VolumeComponent:
        return getitem(self, "components", Identifiable.of(id))

    def add_component(self, component: VolumeComponent) -> VolumeComponent:
        component.generate(self)
        return additem(self, "components", component, component.id, VolumeComponent)

    def remove_component(self, id: Identifiable) -> VolumeComponent:
        return removeitem(self, "components", Identifiable.of(id))

    def clear_components(self) -> Self:
        """Remove all components"""
        return clearitems(self, "components")

    # EVENT

    def get_event(self, event: Identifiable) -> Event:
        return getitem(self, "events", Identifiable.of(event))

    def add_event(self, id: Identifiable, event: Event) -> Event:
        if not isinstance(event, Event):
            raise TypeError(
                f"Expected Event but got '{event.__class__.__name__}' instead"
            )
        i = Identifier.of(id)
        if i in self.events:
            event.generate(self)
            self.events[i][event.id] = event
            return event
        obj = {}
        obj[event.id] = event
        self.events[i] = obj
        event.id
        return event

    def remove_event(self, event: Identifiable) -> Event:
        return removeitem(self, "events", Identifiable.of(event))

    def clear_events(self) -> Self:
        """Remove all events"""
        return clearitems(self, "events")

    def generate(self, ctx) -> None: ...


class VolumeLoader(Loader):
    name = "Volume"

    def __init__(self):
        from .schemas import VolumeSchema1

        Loader.__init__(self, Volume)
        self.add_schema(VolumeSchema1, "1.20.50")
