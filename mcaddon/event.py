from typing import Self
from molang import Molang

from .registry import INSTANCE, Registries
from .constant import EventTarget
from .util import getattr2, Identifier

# EVENTS


class Event:
    """Base event class for items and blocks"""

    def __init__(self, target: EventTarget = None):
        self.target = target

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data["target"] = self.target._value_
        return data

    @property
    def target(self) -> EventTarget:
        return getattr(self, "_target", EventTarget.self)

    @target.setter
    def target(self, value: EventTarget):
        if value is None:
            setattr(self, "_target", EventTarget.self)
            return
        if not isinstance(value, EventTarget):
            raise TypeError(
                f"Expected EventTarget but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_target", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "target" in data:
            self.target = EventTarget[data.pop("target")]
        return self


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
    """Apply mob effect to target"""

    id = Identifier("add_mob_effect")

    def __init__(
        self,
        effect: Identifier | str,
        amplifier: int = 0,
        duration: float = 0.0,
        target: EventTarget = None,
    ):
        Event.__init__(self, target)
        self.effect = Identifier(effect)
        self.amplifier = amplifier
        self.duration = duration
        self.target = target

    @property
    def __dict__(self):
        data = {
            "amplifier": self.amplifier,
            "duration": self.duration,
            "effect": str(self.effect),
        }
        if self.target not in [None, EventTarget.self]:
            data["target"] = self.target._value_
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.amplifier = data.pop("amplifier")
        self.duration = data.pop("duration")
        self.effect = Identifier(data.pop("effect"))
        return self

    @property
    def effect(self) -> Identifier:
        return getattr(self, "_effect")

    @effect.setter
    def effect(self, value: Identifier):
        if isinstance(value, Identifier):
            setattr(self, "_effect", value)
        else:
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )

    @property
    def amplifier(self) -> int:
        return getattr(self, "_amplifier")

    @amplifier.setter
    def amplifier(self, value: int):
        if isinstance(value, int):
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
            setattr(self, "_duration", value)
        else:
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )


@event_type
class Damage(Event):
    """Deals damage to the target"""

    id = Identifier("damage")

    def __init__(
        self,
        type: Identifier | str,
        amount: int = 0,
        mob_amount: int = 0,
        target: EventTarget = None,
    ):
        Event.__init__(self, target)
        self.type = Identifier(type)
        self.amount = amount
        self.mob_amount = mob_amount
        self.target = target

    @property
    def __dict__(self):
        data = {
            "type": str(self.type),
            "amount": self.amount,
            "mob_amount": self.mob_amount,
        }
        if self.target not in [None, EventTarget.self]:
            data["target"] = self.target._value_
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.type = Identifier(data.pop("type"))
        self.amount = data.pop("amount")
        self.mob_amount = data.pop("mob_amount")
        return self

    @property
    def type(self) -> Identifier:
        return getattr(self, "_type")

    @type.setter
    def type(self, value: Identifier):
        if isinstance(value, Identifier):
            setattr(self, "_type", value)
        else:
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )

    @property
    def amount(self) -> int:
        return getattr(self, "_amount")

    @amount.setter
    def amount(self, value: int):
        if isinstance(value, int):
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
            setattr(self, "_mob_amount", value)
        else:
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )


@event_type
class DecrementStack(Event):
    """Decrement item stack"""

    id = Identifier("decrement_stack")

    def __init__(self, target: EventTarget = None):
        Event.__init__(self, target)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        return self

    @property
    def __dict__(self):
        data = {}
        return data


@event_type
class Die(Event):
    """Kill target. If target is self and this is run from a block then destroy the block"""

    id = Identifier("die")

    def __init__(self, target: EventTarget = None):
        Event.__init__(self, target)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        return self

    @property
    def __dict__(self):
        data = {}
        if self.target not in [None, EventTarget.self]:
            data["target"] = self.target._value_
        return data


@event_type
class PlayEffect(Event):
    """Spawns a particle effect relative to target position"""

    id = Identifier("play_effect")

    def __init__(
        self, effect: Identifier | str, data: int = 0, target: EventTarget = None
    ):
        Event.__init__(self, target)
        self.effect = Identifier(effect)
        self.data = data
        self.target = target

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.effect = Identifier(data.pop("effect"))
        self.data = data.pop("data")
        return self

    @property
    def __dict__(self):
        data = {"effect": str(self.effect), "data": self.data}
        if self.target not in [None, EventTarget.self]:
            data["target"] = self.target._value_
        return data

    @property
    def effect(self) -> Identifier:
        return getattr(self, "_effect")

    @effect.setter
    def effect(self, value: Identifier):
        if isinstance(value, Identifier):
            setattr(self, "_effect", value)
        else:
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )

    @property
    def data(self) -> int:
        return getattr(self, "_data")

    @data.setter
    def data(self, value: int):
        if isinstance(value, int):
            setattr(self, "_data", value)
        else:
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )


@event_type
class PlaySound(Event):
    """Play a sound relative to target position"""

    id = Identifier("play_sound")

    def __init__(self, sound: str, target: EventTarget = None):
        Event.__init__(self, target)
        self.sound = sound
        self.target = target

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.sound = Identifier(data.pop("sound"))
        return self

    @property
    def __dict__(self):
        data = {"sound": str(self.sound)}
        if self.target not in [None, EventTarget.self]:
            data["target"] = self.target._value_
        return data

    @property
    def sound(self) -> str:
        return getattr(self, "_sound")

    @sound.setter
    def sound(self, value: str):
        setattr(self, "_sound", str(value))


@event_type
class RemoveMobEffect(Event):
    """Removes mob effect from target"""

    id = Identifier("remove_mob_effect")

    def __init__(self, effect: Identifier | str, target: EventTarget = None):
        Event.__init__(self, target)
        self.effect = Identifier(effect)
        self.target = target

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.effect = Identifier(data.pop("effect"))
        return self

    @property
    def __dict__(self):
        data = {"effect": str(self.effect)}
        if self.target not in [None, EventTarget.self]:
            data["target"] = self.target._value_
        return data

    @property
    def effect(self) -> Identifier:
        return getattr(self, "_effect")

    @effect.setter
    def effect(self, value: Identifier):
        if isinstance(value, Identifier):
            setattr(self, "_effect", value)
        else:
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )


@event_type
class RunCommand(Event):
    """Triggers a slash command or a list of slash commands"""

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

    @property
    def __dict__(self):
        data = {"command": self.command}
        if isinstance(self.command, list) and len(self.command) == 1:
            data["command"] = self.command[0]
        if self.target not in [None, EventTarget.self]:
            data["target"] = self.target._value_
        return data

    @property
    def command(self) -> list[str]:
        return getattr(self, "_command")

    @command.setter
    def command(self, value: list[str]):
        if isinstance(value, list):
            setattr(self, "_command", [str(x) for x in value])
        else:
            self.command = [str(value)]


@event_type
class SetBlock(Event):
    """Sets this block to another block type"""

    id = Identifier("set_block")

    def __init__(self, block_type: Identifier | str):
        self.block_type = Identifier(block_type)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.block_type = Identifier(data.pop("block_type"))
        return self

    @property
    def __dict__(self):
        data = {"block_type": str(self.block_type)}
        return data

    @property
    def block_type(self) -> Identifier:
        return getattr(self, "_block_type")

    @block_type.setter
    def block_type(self, value: Identifier):
        if not isinstance(value, Identifier):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_block_type", value)


@event_type
class SetBlockAtPos(Event):
    """Sets a block relative to this block to another block type"""

    id = Identifier("set_block_at_pos")

    def __init__(
        self, block_type: Identifier | str, block_offset: list = [0.0, 0.0, 0.0]
    ):
        self.block_type = Identifier(block_type)
        self.block_offset = block_offset

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().from_dict(data)
        self.block_type = Identifier(data.pop("block_type"))
        self.block_offset = data.pop("block_offset")
        return self

    @property
    def __dict__(self):
        data = {"block_type": str(self.block_type), "block_offset": self.block_offset}
        return data

    @property
    def block_type(self) -> Identifier:
        return getattr(self, "_block_type")

    @block_type.setter
    def block_type(self, value: Identifier):
        if not isinstance(value, Identifier):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_block_type", value)

    @property
    def block_offset(self) -> list:
        return getattr(self, "_block_offset")

    @block_offset.setter
    def block_offset(self, value: list):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_block_offset", value)


@event_type
class SpawnLoot(Event):
    """Spawn loot from block"""

    id = Identifier("spawn_loot")

    def __init__(self, table: str):
        self.table = table

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = super().__init__(data)
        self.table = data.pop("table")
        return self

    @property
    def __dict__(self):
        data = {"table": str(self.table)}
        return data

    @property
    def table(self) -> str:
        return getattr(self, "_table")

    @table.setter
    def table(self, value: str):
        setattr(self, "_table", str(value))


@event_type
class Swing(Event):
    """Event causes the actor to swing"""

    id = Identifier("swing")

    def __init__(self, target: EventTarget = None):
        Event.__init__(self, target)

    @property
    def __dict__(self):
        data = {}
        return data


@event_type
class Teleport(Event):
    """Teleport target randomly around destination point"""

    id = Identifier("teleport")

    def __init__(
        self,
        avoid_water: bool = True,
        destination: list = [0.0, 0.0, 0.0],
        land_on_block: bool = True,
        max_range: list = [8.0, 8.0, 8.0],
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
        self.destination = data.pop("destination")
        self.land_on_block = data.pop("land_on_block")
        self.max_range = data.pop("max_range")
        return self

    @property
    def __dict__(self):
        data = {
            "avoid_water": self.avoid_water,
            "destination": self.destination,
            "land_on_block": self.land_on_block,
            "max_range": self.max_range,
        }
        if self.target not in [None, EventTarget.self]:
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
        setattr(self, "_avoid_water", value)

    @property
    def destination(self) -> list:
        return getattr(self, "_destination")

    @destination.setter
    def destination(self, value: list):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
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
        setattr(self, "_land_on_block", value)

    @property
    def max_range(self) -> list:
        return getattr(self, "_max_range")

    @max_range.setter
    def max_range(self, value: list):
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_max_range", value)


@event_type
class TransformiIem(Event):
    """Transforms item into another item"""

    id = Identifier("transform_item")

    def __init__(self, transform: Identifier | str):
        self.transform = Identifier(transform)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.transform = data
        return self

    @property
    def __dict__(self):
        data = str(self.transform)
        return data

    @property
    def transform(self) -> Identifier:
        return getattr(self, "_transform")

    @transform.setter
    def transform(self, value: Identifier):
        if not isinstance(value, Identifier):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_transform", value)


@event_type
class SetBlockState(Event):
    """Sets a block state on this block"""

    id = Identifier("set_block_state")

    def __init__(self, states: dict[Identifier, Molang] = {}, **state: str):
        self.states = states

    @property
    def __dict__(self):
        data = {}
        for k, v in self.states.items():
            data[str(k)] = str(v)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        for k, v in data.items():
            id = Identifier(k)
            self.states[id] = Molang(v)
        return self

    @property
    def states(self) -> dict[Identifier, Molang]:
        return getattr2(self, "_states", {})

    @states.setter
    def states(self, value: dict[Identifier, Molang]):
        if not isinstance(value, dict):
            raise TypeError(
                f"Expected dict but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_states", value)


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

    @property
    def __dict__(self):
        data = []
        for v in self.events:
            data.append({})
            if v["condition"] is not None:
                data[-1]["condition"] = str(v["condition"])
            for i, j in v["events"].items():
                data[-1][i.path] = j.__dict__
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
    """Randomly run event responses"""

    id = Identifier("randomize")
    pass


@event_type
class Trigger(Event):
    """Trigger an event on a specified target"""

    id = Identifier("trigger")

    def __init__(
        self, event: Identifier | str, condition: Molang = None, target: str = None
    ):
        Event.__init__(self, target)
        self.event = event
        self.condition = None if condition is None else Molang(condition)
        self.target = target

    @property
    def __dict__(self) -> dict:
        data = {"event": str(self.event)}
        if self.target not in [None, EventTarget.self]:
            data["target"] = self.target._value_
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
    def event(self, value: Identifier | str):
        if isinstance(value, (Identifier, str)):
            setattr(self, "_event", Identifier(value))
        else:
            raise TypeError(
                f"Expected Molang but got '{value.__class__.__name__}' instead"
            )

    @property
    def target(self) -> str:
        """The target of event executed on the object"""
        return getattr(self, "_target")

    @target.setter
    def target(self, value: str):
        setattr(self, "_target", str(value))


# CUSTOM


class IncrementBlockState(SetBlockState):
    """Increase a block state on this block"""

    def __init__(self, name: Identifier, amount: int = 1):
        id = Identifier(name)
        SetBlockState.__init__(self, {id: f"q.block_state('{id}')+{amount}"})


class DecrementBlockState(SetBlockState):
    """Decrease a block state on this block"""

    def __init__(self, name: Identifier, amount: int = 1):
        id = Identifier(name)
        SetBlockState.__init__(self, {id: f"q.block_state('{id}')-{amount}"})


class SwitchBlockState(SetBlockState):
    """Switch a boolean block state on this block. (true = false, false = true)"""

    def __init__(self, name: Identifier):
        id = Identifier(name)
        SetBlockState.__init__(self, {id: f"!q.block_state('{id}')"})
