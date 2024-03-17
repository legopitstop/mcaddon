from typing import Self
from molang import Molang

from .registry import INSTANCE, Registries
from .constant import EventTarget
from .math import Vector3
from .util import (
    getattr2,
    clearitems,
    getitem,
    removeitem,
    additem,
    Identifier,
    Identifiable,
    Misc,
)

# EVENTS


class Event(Misc):
    """Base event class for items and blocks"""

    def __init__(self, target: EventTarget = None):
        self.target = target

    def __call__(self, ctx) -> int:
        return self.execute(ctx)

    def jsonify(self) -> dict:
        data = super().jsonify()
        data["target"] = self.target.jsonify()

        return data

    @property
    def target(self) -> EventTarget:
        return getattr(self, "_target", EventTarget.SELF)

    @target.setter
    def target(self, value: EventTarget):
        if value is None:
            self.target = EventTarget.SELF
            return
        if not isinstance(value, EventTarget):
            raise TypeError(
                f"Expected EventTarget but got '{value.__class__.__name__}' instead"
            )
        self.on_update("target", value)
        setattr(self, "_target", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "target" in data:
            self.target = EventTarget.from_dict(data.pop("target"))
        return self

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifier):
        setattr(self, "_id", Identifier.of(value))

    def generate(self, ctx) -> None:
        """
        Called when this event is added to Item, Block, Volume, or BehaviorPack

        :type ctx: Item | Block | Volume | BehaviorPack
        """
        ...

    def execute(self, ctx) -> int:
        return 0


INSTANCE.create_registry(Registries.EVENT_TYPE, Event)


def event_type(cls):
    """
    Add this event to the registry
    """

    def wrapper():
        if not issubclass(cls, Event):
            raise TypeError(f"Expected Event but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.EVENT_TYPE, cls.id, cls)

    return wrapper()


@event_type
class AddMobEffect(Event):
    """Apply mob effect to target. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_add_mob_effect?view=minecraft-bedrock-stable)"""

    id = Identifier("add_mob_effect")

    def __init__(
        self,
        effect: Identifiable,
        amplifier: int = 0,
        duration: float = 0.0,
        target: EventTarget = None,
    ):
        Event.__init__(self, target)
        self.effect = effect
        self.amplifier = amplifier
        self.duration = duration
        self.target = target

    def jsonify(self):
        data = {
            "amplifier": self.amplifier,
            "duration": self.duration,
            "effect": str(self.effect),
        }
        if self.target not in [None, EventTarget.SELF]:
            data["target"] = self.target._value_
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.amplifier = data.pop("amplifier")
        self.duration = data.pop("duration")
        self.effect = data.pop("effect")
        return self

    @property
    def effect(self) -> Identifier:
        return getattr(self, "_effect")

    @effect.setter
    def effect(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("effect", id)
        setattr(self, "_effect", id)

    @property
    def amplifier(self) -> int:
        return getattr(self, "_amplifier")

    @amplifier.setter
    def amplifier(self, value: int):
        if isinstance(value, int):
            self.on_update("amplifier", value)
            setattr(self, "_amplifier", value)
        else:
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )

    @property
    def duration(self) -> float:
        return getattr(self, "_duration")

    @duration.setter
    def duration(self, value: float):
        if isinstance(value, float):
            self.on_update("duration", value)
            setattr(self, "_duration", value)
        else:
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )


@event_type
class Damage(Event):
    """Deals damage to the target. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_damage?view=minecraft-bedrock-stable)"""

    id = Identifier("damage")

    def __init__(
        self,
        type: Identifiable,
        amount: int = 0,
        mob_amount: int = 0,
        target: EventTarget = None,
    ):
        Event.__init__(self, target)
        self.type = type
        self.amount = amount
        self.mob_amount = mob_amount
        self.target = target

    def jsonify(self):
        data = {
            "type": str(self.type),
            "amount": self.amount,
            "mob_amount": self.mob_amount,
        }
        if self.target not in [None, EventTarget.SELF]:
            data["target"] = self.target._value_
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.type = data.pop("type")
        self.amount = data.pop("amount")
        self.mob_amount = data.pop("mob_amount")
        return self

    @staticmethod
    def item(amount: int = 1):
        return Damage("durability", amount, target=EventTarget.ITEM)

    @property
    def type(self) -> Identifier:
        return getattr(self, "_type")

    @type.setter
    def type(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("type", id)
        setattr(self, "_type", id)

    @property
    def amount(self) -> int:
        return getattr(self, "_amount")

    @amount.setter
    def amount(self, value: int):
        if isinstance(value, int):
            self.on_update("amount", value)
            setattr(self, "_amount", value)
        else:
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )

    @property
    def mob_amount(self) -> int:
        return getattr(self, "_mob_amount")

    @mob_amount.setter
    def mob_amount(self, value: int):
        if isinstance(value, int):
            self.on_update("mob_amount", value)
            setattr(self, "_mob_amount", value)
        else:
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )


@event_type
class DecrementStack(Event):
    """Decrement item stack. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_decrement_stack?view=minecraft-bedrock-stable)"""

    id = Identifier("decrement_stack")

    def __init__(self, target: EventTarget = None):
        Event.__init__(self, target)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        return self

    def jsonify(self):
        data = {}
        return data


@event_type
class Die(Event):
    """Kill target. If target is self and this is run from a block then destroy the block. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_die?view=minecraft-bedrock-stable)"""

    id = Identifier("die")

    def __init__(self, target: EventTarget = None):
        Event.__init__(self, target)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        return self

    def jsonify(self):
        data = {}
        if self.target not in [None, EventTarget.SELF]:
            data["target"] = self.target._value_
        return data


@event_type
class PlayEffect(Event):
    """Spawns a particle effect relative to target position. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_play_effect?view=minecraft-bedrock-stable)"""

    id = Identifier("play_effect")

    def __init__(self, effect: Identifiable, data: int = 0, target: EventTarget = None):
        Event.__init__(self, target)
        self.effect = effect
        self.data = data
        self.target = target

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.effect = data.pop("effect")
        self.data = data.pop("data")
        return self

    def jsonify(self):
        data = {"effect": str(self.effect), "data": self.data}
        if self.target not in [None, EventTarget.SELF]:
            data["target"] = self.target._value_
        return data

    @property
    def effect(self) -> Identifier:
        return getattr(self, "_effect")

    @effect.setter
    def effect(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("effect", id)
        setattr(self, "_effect", id)

    @property
    def data(self) -> int:
        return getattr(self, "_data")

    @data.setter
    def data(self, value: int):
        if isinstance(value, int):
            self.on_update("data", value)
            setattr(self, "_data", value)
        else:
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )


@event_type
class PlaySound(Event):
    """Play a sound relative to target position. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_play_sound?view=minecraft-bedrock-stable)"""

    id = Identifier("play_sound")

    def __init__(self, sound: Identifiable, target: EventTarget = None):
        Event.__init__(self, target)
        self.sound = sound
        self.target = target

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.sound = data.pop("sound")
        return self

    def jsonify(self):
        data = {"sound": str(self.sound)}
        if self.target not in [None, EventTarget.SELF]:
            data["target"] = self.target._value_
        return data

    @property
    def sound(self) -> Identifier:
        return getattr(self, "_sound")

    @sound.setter
    def sound(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("sound", id)
        setattr(self, "_sound", id)


@event_type
class RemoveMobEffect(Event):
    """Removes mob effect from target. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_remove_mob_effect?view=minecraft-bedrock-stable)"""

    id = Identifier("remove_mob_effect")

    def __init__(self, effect: Identifiable, target: EventTarget = None):
        Event.__init__(self, target)
        self.effect = effect
        self.target = target

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.effect = data.pop("effect")
        return self

    def jsonify(self):
        data = {"effect": str(self.effect)}
        if self.target not in [None, EventTarget.SELF]:
            data["target"] = self.target._value_
        return data

    @property
    def effect(self) -> Identifier:
        return getattr(self, "_effect")

    @effect.setter
    def effect(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("effect", id)
        setattr(self, "_effect", id)


@event_type
class RunCommand(Event):
    """Triggers a slash command or a list of slash commands. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_run_command?view=minecraft-bedrock-stable)"""

    id = Identifier("run_command")

    def __init__(self, command: str | list[str], target: EventTarget = None):
        Event.__init__(self, target)
        self.command = command
        self.target = target

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.command = data.pop("command")
        return self

    def jsonify(self):
        data = {"command": self.command}
        if isinstance(self.command, list) and len(self.command) == 1:
            data["command"] = self.command[0]
        if self.target not in [None, EventTarget.SELF]:
            data["target"] = self.target._value_
        return data

    @property
    def command(self) -> list[str]:
        return getattr(self, "_command")

    @command.setter
    def command(self, value: list[str]):
        if isinstance(value, list):
            v = [str(x) for x in value]
            self.on_update("command", v)
            setattr(self, "_command", v)
        else:
            self.command = [str(value)]

    def get_command(self, index: int) -> str:
        return getitem(self, "commands", index)

    def add_commands(self, command: str) -> str:
        return additem(self, "commands", command)

    def remove_command(self, index: int) -> str:
        return removeitem(self, "commands", index)

    def clear_commands(self) -> Self:
        """Remove all commands"""
        return clearitems(self, "commands")


@event_type
class SetBlock(Event):
    """Sets this block to another block type. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_set_block?view=minecraft-bedrock-stable)"""

    id = Identifier("set_block")

    def __init__(self, block_type: Identifiable):
        self.block_type = block_type

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.block_type = data.pop("block_type")
        return self

    def jsonify(self):
        data = {"block_type": str(self.block_type)}
        return data

    @property
    def block_type(self) -> Identifier:
        return getattr(self, "_block_type")

    @block_type.setter
    def block_type(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("block_type", id)
        setattr(self, "_block_type", id)


@event_type
class SetBlockAtPos(Event):
    """Sets a block relative to this block to another block type. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_set_block_at_pos?view=minecraft-bedrock-stable)"""

    id = Identifier("set_block_at_pos")

    def __init__(
        self, block_type: Identifiable, block_offset: Vector3 = Vector3(0, 0, 0)
    ):
        self.block_type = block_type
        self.block_offset = block_offset

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.block_type = data.pop("block_type")
        self.block_offset = Vector3.from_dict(data.pop("block_offset"))
        return self

    def jsonify(self):
        data = {
            "block_type": str(self.block_type),
            "block_offset": self.block_offset.jsonify(),
        }
        return data

    @property
    def block_type(self) -> Identifier:
        return getattr(self, "_block_type")

    @block_type.setter
    def block_type(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("block_type", id)
        setattr(self, "_block_type", id)

    @property
    def block_offset(self) -> Vector3:
        return getattr(self, "_block_offset")

    @block_offset.setter
    def block_offset(self, value: Vector3):
        if not isinstance(value, Vector3):
            raise TypeError(
                f"Expected Vector3 but got '{value.__class__.__name__}' instead"
            )
        self.on_update("block_offset", value)
        setattr(self, "_block_offset", value)


@event_type
class SpawnLoot(Event):
    """Spawn loot from block. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_spawn_loot?view=minecraft-bedrock-stable)"""

    id = Identifier("spawn_loot")

    def __init__(self, table: str):
        self.table = table

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().__init__(data)
        self.table = data.pop("table")
        return self

    def jsonify(self):
        data = {"table": str(self.table)}
        return data

    @property
    def table(self) -> str:
        return getattr(self, "_table")

    @table.setter
    def table(self, value: str):
        self.on_update("table", str(value))
        setattr(self, "_table", str(value))


@event_type
class Swing(Event):
    """Event causes the actor to swing. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_swing?view=minecraft-bedrock-stable)"""

    id = Identifier("swing")

    def __init__(self, target: EventTarget = None):
        Event.__init__(self, target)

    def jsonify(self):
        data = {}
        return data


@event_type
class Teleport(Event):
    """Teleport target randomly around destination point. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_teleport?view=minecraft-bedrock-stable)"""

    id = Identifier("teleport")

    def __init__(
        self,
        avoid_water: bool = True,
        destination: Vector3 = Vector3(0.0, 0.0, 0.0),
        land_on_block: bool = True,
        max_range: Vector3 = Vector3(8.0, 8.0, 8.0),
        target: EventTarget = None,
    ):
        self.avoid_water = avoid_water
        self.destination = destination
        self.land_on_block = land_on_block
        self.max_range = max_range
        self.target = target

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.avoid_water = data.pop("avoid_water")
        self.destination = Vector3.from_dict(data.pop("destination"))
        self.land_on_block = data.pop("land_on_block")
        self.max_range = Vector3.from_dict(data.pop("max_range"))
        return self

    def jsonify(self):
        data = {
            "avoid_water": self.avoid_water,
            "destination": self.destination.jsonify(),
            "land_on_block": self.land_on_block,
            "max_range": self.max_range.jsonify(),
        }
        if self.target not in [None, EventTarget.SELF]:
            data["target"] = self.target._value_
        return data

    @property
    def avoid_water(self) -> bool:
        return getattr(self, "_avoid_water")

    @avoid_water.setter
    def avoid_water(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("avoid_water", value)
        setattr(self, "_avoid_water", value)

    @property
    def destination(self) -> Vector3:
        return getattr(self, "_destination")

    @destination.setter
    def destination(self, value: Vector3):
        if not isinstance(value, Vector3):
            raise TypeError(
                f"Expected Vector3 but got '{value.__class__.__name__}' instead"
            )
        self.on_update("destination", value)
        setattr(self, "_destination", value)

    @property
    def land_on_block(self) -> bool:
        return getattr(self, "_land_on_block")

    @land_on_block.setter
    def land_on_block(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        self.on_update("land_on_block", value)
        setattr(self, "_land_on_block", value)

    @property
    def max_range(self) -> Vector3:
        return getattr(self, "_max_range")

    @max_range.setter
    def max_range(self, value: Vector3):
        if not isinstance(value, Vector3):
            raise TypeError(
                f"Expected Vector3 but got '{value.__class__.__name__}' instead"
            )
        self.on_update("max_range", value)
        setattr(self, "_max_range", value)


@event_type
class TransformIem(Event):
    """Transforms item into another item. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_transform_item?view=minecraft-bedrock-stable)"""

    id = Identifier("transform_item")

    def __init__(self, transform: Identifiable):
        self.transform = transform

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.transform = data
        return self

    def jsonify(self):
        data = str(self.transform)
        return data

    @property
    def transform(self) -> Identifier:
        return getattr(self, "_transform")

    @transform.setter
    def transform(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("transform", id)
        setattr(self, "_transform", id)


@event_type
class SetBlockProperty(Event):
    """Sets a block state on this block. [MS Docs](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockevents/minecraftblock_set_block_state?view=minecraft-bedrock-stable)"""

    id = Identifier("set_block_state")

    def __init__(self, states: dict[Identifiable, Molang] = {}):
        self.states = states

    def jsonify(self):
        data = {}
        for k, v in self.states.items():
            data[str(k)] = Molang(v)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        for k, v in data.items():
            id = Identifiable.of(k)
            self.states[id] = Molang(v)
        return self

    @property
    def states(self) -> dict[Identifier, Molang]:
        return getattr2(self, "_states", {})

    @states.setter
    def states(self, value: dict[Identifiable, Molang]):
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        states = {}
        for k, v in value.items():
            id = Identifiable.of(k)
            states[id] = v
        self.on_update("states", states)
        setattr(self, "_states", states)

    def get_state(self, name: Identifiable) -> Identifier:
        return getitem(self, "states", Identifiable.of(name))

    def add_state(self, name: Identifiable, value: Molang) -> Self:
        return additem(self, "states", Molang(value), Identifiable.of(name))

    def remove_state(self, name: Identifiable) -> Molang:
        return removeitem(self, "states", Identifiable.of(name))

    def clear_states(self) -> Self:
        """Remove all states"""
        return clearitems(self, "states")


@event_type
class Sequence(Event):
    """Run the same response multiple times, or to only trigger certain aspects of your event when conditions are met."""

    id = Identifier("sequence")

    def __init__(self):
        self.events = []

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "condition" in data:
            self.condition
        self.events = [x for x in data]
        return self

    def jsonify(self):
        data = []
        for v in self.events:
            data.append({})
            if v["condition"] is not None:
                data[-1]["condition"] = str(v["condition"])
            for i, j in v["events"].items():
                data[-1][i.path] = j.jsonify()
        return data

    @property
    def events(self) -> list[dict]:
        return getattr(self, "_events")

    @events.setter
    def events(self, value: list[dict]):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list[Event] but got '{value.__class__.__name__}' instead"
            )
        self.on_update("events", value)
        setattr(self, "_events", value)

    # CONDITION

    def set_condition(self, index: int, condition: Molang) -> Molang:
        c = condition if isinstance(condition, Molang) else Molang(condition)
        if not self.event_exists(index):
            self.events.insert(index, {"events": {}, "condition": None})
        self.events[index]["condition"] = condition
        return c

    def get_condition(self, index: int) -> Molang:
        return self.events[int(index)]["condition"]

    def remove_condition(self, index: int) -> Molang:
        e = self.events[int(index)]["condition"]
        self.events[int(index)]["condition"] = None
        return e

    # EVENT

    def event_exists(self, index: int) -> bool:
        return (0 <= index) and (index < len(self.events))

    def add_event(self, index: int, event: Event) -> Event:
        if not isinstance(event, Event):
            raise TypeError(
                f"Expected Event but got '{event.__class__.__name__}' instead"
            )
        if not self.event_exists(index):
            self.events.insert(index, {"events": {}, "condition": None})
        self.events[index]["events"][event.id] = event
        return event

    def get_event(self, index: int) -> Event:
        return self.events[int(index)]["events"]

    def remove_event(self, index: int) -> Event:
        e = self.events[int(index)]
        del self.events[int(index)]
        return e

    def clear_events(self) -> Self:
        self.events = []
        return self


@event_type
class Randomize(Sequence):
    """Randomly run event responses."""

    id = Identifier("randomize")
    pass


@event_type
class Trigger(Event):
    """Trigger an event on a specified target."""

    id = Identifier("trigger")

    def __init__(
        self, event: Identifiable, condition: Molang = None, target: str = None
    ):
        Event.__init__(self, target)
        self.event = event
        self.condition = None if condition is None else Molang(condition)
        self.target = target

    def jsonify(self) -> dict:
        data = {"event": str(self.event)}
        if self.target not in [None, EventTarget.SELF]:
            data["target"] = (
                self.target._value_
                if isinstance(self.target, EventTarget)
                else self.target
            )
        if hasattr(self, "condition") and self.condition:
            data["condition"] = str(self.condition)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.event = data.pop("event")
        if "condition" in data:
            self.condition = Molang(data.pop("condition"))
        return self

    @property
    def condition(self) -> Molang:
        """The condition of event to be executed on the object, defaults to None"""
        return getattr(self, "_condition")

    @condition.setter
    def condition(self, value: Molang):
        if value is None:
            setattr(self, "_condition", None)
        elif isinstance(value, Molang):
            self.on_update("condition", value)
            setattr(self, "_condition", value)
        else:
            raise TypeError(
                f"Expected Molang but got '{value.__class__.__name__}' instead"
            )

    @property
    def event(self) -> Identifier:
        """The event executed on the block"""
        return getattr(self, "_event")

    @event.setter
    def event(self, value: Identifiable | str):
        id = Identifiable.of(value)
        self.on_update("event", id)
        setattr(self, "_event", id)

    @property
    def target(self) -> EventTarget:
        """The target of event executed on the object"""
        return getattr(self, "_target", EventTarget.SELF)

    @target.setter
    def target(self, value: EventTarget):
        if value is None:
            self.target = EventTarget.SELF
            return
        if not isinstance(value, EventTarget):
            raise TypeError(
                f"Expected EventTarget but got '{value.__class__.__name__}' instead"
            )
        self.on_update("target", value)
        setattr(self, "_target", value)


# CUSTOM


class IncrementBlockProperty(SetBlockProperty):
    """Increase a block state on this block"""

    def __init__(self, name: Identifiable, count: int = 1):
        id = Identifiable.of(name)
        SetBlockProperty.__init__(self, {id: f"q.block_state('{id}')+{count}"})


class DecrementBlockProperty(SetBlockProperty):
    """Decrease a block state on this block"""

    def __init__(self, name: Identifiable, count: int = 1):
        id = Identifiable.of(name)
        SetBlockProperty.__init__(self, {id: f"q.block_state('{id}')-{count}"})


class SwitchBlockProperty(SetBlockProperty):
    """Switch a boolean block state on this block. (true -> false, false -> true)"""

    def __init__(self, name: Identifiable):
        id = Identifiable.of(name)
        SetBlockProperty.__init__(self, {id: f"!q.block_state('{id}')"})
