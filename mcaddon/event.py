from typing import Self

from .constant import EventTarget
from .util import Identifier, Molang

# Events

class Event:
    def __init__(self, target:EventTarget=None):
        """
        Base event class for items and blocks

        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: EventTarget, optional
        """
        self.target = target
    
    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        data['target'] = self.target._value_
        return data

    @property
    def target(self) -> EventTarget:
        return getattr(self, '_target')
    
    @target.setter
    def target(self, value:EventTarget):
        if value is None:
            setattr(self, '_target', value)
            return
        if not isinstance(value, EventTarget): raise TypeError(f"Expected EventTarget but got '{value.__class__.__name__}' instead")
        setattr(self, '_target', value)

    @classmethod
    def from_dict(cls, data:dict) -> Self:
        raise NotImplementedError()

EVENTS:dict[str, Event] = {}
def event(id:Identifier|str):
    """
    Add this event to the parser

    :param id: The ID of this event
    :type id: Identifier | str
    """
    def wrapper(cls):
        global EVENTS
        id2 = Identifier.parse(id)
        cls.id = id2
        EVENTS[str(id2)] = cls
        return cls
    return wrapper

@event('add_mob_effect')
class AddMobEffect(Event):
    def __init__(self,  effect:Identifier|str, amplifier:int=0, duration:float=0.0, target:EventTarget=None):
        """
        Apply mob effect to target

        :param effect: The mob effect to apply
        :type effect: Identifier | str
        :param amplifier: The amplifier for the mob effect, defaults to 0
        :type amplifier: int, optional
        :param duration: The duration of the mob effect, defaults to 0.0
        :type duration: float, optional
        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: EventTarget, optional
        """
        Event.__init__(self, target)
        self.effect = Identifier.parse(effect)
        self.amplifier = amplifier
        self.duration = duration
        self.target = target
        
    @property
    def __dict__(self):
        data = {
            'amplifier': self.amplifier,
            'duration': self.duration,
            'effect': str(self.effect)
        }
        if self.target not in [None, EventTarget.SELF]: data['target'] = self.target._value_
        return data
    
    @property
    def effect(self) -> Identifier:
        return getattr(self, '_effect')
    
    @effect.setter
    def effect(self, value:Identifier):
        if isinstance(value, Identifier):
            setattr(self, '_effect', value)
        else:
            raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
    
    @property
    def amplifier(self) -> int:
        return getattr(self, '_amplifier')
    
    @amplifier.setter
    def amplifier(self, value:int):
        if isinstance(value, int):
            setattr(self, '_amplifier', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        
    @property
    def duration(self) -> float:
        return getattr(self, '_duration')
    
    @duration.setter
    def duration(self, value:float):
        if isinstance(value, float):
            setattr(self, '_duration', value)
        else:
            raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        
@event('damage')
class Damage(Event):
    def __init__(self, type:Identifier|str, amount:int=0, mob_amount:int=0, target:EventTarget=None):
        """
        Deals damage to the target

        :param type: The type of damage to deal
        :type type: Identifier | str
        :param amount: The amount of damage to deal, defaults to 0
        :type amount: int, optional
        :param mob_amount: The amount of damage to deal if held by a mob, defaults to 0
        :type mob_amount: int, optional
        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: EventTarget, optional
        """
        Event.__init__(self, target)
        self.type = Identifier.parse(type)
        self.amount = amount
        self.mob_amount = mob_amount
        self.target = target
        
    @property
    def __dict__(self):
        data = {
            'type': str(self.type),
            'amount': self.amount,
            'mob_amount': self.mob_amount
        }
        if self.target not in [None, EventTarget.SELF]: data['target'] = self.target._value_
        return data
    
    @property
    def type(self) -> Identifier:
        return getattr(self, '_type')
    
    @type.setter
    def type(self, value:Identifier):
        if isinstance(value, Identifier):
            setattr(self, '_type', value)
        else:
            raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        
    @property
    def amount(self) -> int:
        return getattr(self, '_amount')
    
    @amount.setter
    def amount(self, value:int):
        if isinstance(value, int):
            setattr(self, '_amount', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
    
    @property
    def mob_amount(self) -> int:
        return getattr(self, '_mob_amount')
    
    @mob_amount.setter
    def mob_amount(self, value:int):
        if isinstance(value, int):
            setattr(self, '_mob_amount', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
    
@event('decrement_stack')
class DecrementStack(Event):
    def __init__(self, target:EventTarget=None):
        """
        Decrement item stack

        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: EventTarget, optional
        """
        Event.__init__(self, target)

    @property
    def __dict__(self):
        data = {}
        return data
        
@event('die')
class Die(Event):
    def __init__(self, target:EventTarget=None):
        """
        Kill target. If target is self and this is run from a block then destroy the block

        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: EventTarget, optional
        """
        Event.__init__(self, target)
        
    @property
    def __dict__(self):
        data = {}
        if self.target not in [None, EventTarget.SELF]: data['target'] = self.target._value_
        return data
        
@event('play_effect')
class PlayEffect(Event):
    def __init__(self, effect:Identifier|str, data:int=0, target:EventTarget=None):
        """
        Spawns a particle effect relative to target position

        :param effect: The name of the particle effect to create
        :type effect: Identifier | str
        :param data: Particle data value, defaults to 0
        :type data: int, optional
        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: EventTarget, optional
        """
        Event.__init__(self, target)
        self.effect = Identifier.parse(effect)
        self.data = data
        self.target = target
        
    @property
    def __dict__(self):
        data = {
            'effect': str(self.effect),
            'data': self.data
        }
        if self.target not in [None, EventTarget.SELF]: data['target'] = self.target._value_
        return data
        
    @property
    def effect(self) -> Identifier:
        return getattr(self, '_effect')
    
    @effect.setter
    def effect(self, value:Identifier):
        if isinstance(value, Identifier):
            setattr(self, '_effect', value)
        else:
            raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")

    @property
    def data(self) -> int:
        return getattr(self, '_data')
    
    @data.setter
    def data(self, value:int):
        if isinstance(value, int):
            setattr(self, '_data', value)
        else:
            raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")

@event('play_sound')
class PlaySound(Event):
    def __init__(self, sound:str, target:EventTarget=None):
        """
        Play a sound relative to target position

        :param sound: The name of the sound to play
        :type sound: str
        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: EventTarget, optional
        """
        Event.__init__(self, target)
        self.sound = sound
        self.target = target
        
    @property
    def __dict__(self):
        data = {
            'sound': str(self.sound)
        }
        if self.target not in [None, EventTarget.SELF]: data['target'] = self.target._value_
        return data
        
    @property
    def sound(self) -> str:
        return getattr(self, '_sound')
    
    @sound.setter
    def sound(self, value:str):
        setattr(self, '_sound', str(value))

@event('remove_mob_effect')
class RemoveMobEffect(Event):
    def __init__(self, effect:Identifier|str, target:EventTarget=None):
        """
        Removes mob effect from target

        :param effect: The mob effect to remove. Use 'all' to remove all mob effects from target
        :type effect: Identifier | str
        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: EventTarget, optional
        """
        Event.__init__(self, target)
        self.effect = Identifier.parse(effect)
        self.target = target
        
    @property
    def __dict__(self):
        data = {
            'effect': str(self.effect)
        }
        if self.target not in [None, EventTarget.SELF]: data['target'] = self.target._value_
        return data
    
    @property
    def effect(self) -> Identifier:
        return getattr(self, '_effect')
    
    @effect.setter
    def effect(self, value:Identifier):
        if isinstance(value, Identifier):
            setattr(self, '_effect', value)
        else:
            raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        
@event('run_command')
class RunCommand(Event):
    def __init__(self, command:str|list[str], target:EventTarget=None):
        """
        Triggers a slash command or a list of slash commands

        :param command: Slash command(s) to run
        :type command: str | list[str]
        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: EventTarget, optional
        """
        Event.__init__(self, target)
        self.command = command
        self.target = target
        
    @property
    def __dict__(self):
        data = {
            'command': self.command
        }
        if self.target not in [None, EventTarget.SELF]: data['target'] = self.target._value_
        return data
    
    @property
    def command(self) -> list[str]:
        return getattr(self, '_command')
    
    @command.setter
    def command(self, value:list[str]):
        if isinstance(value, list):
            setattr(self, '_command', [str(x) for x in value])
        else:
            self.command = [str(value)]
        
@event('set_block')
class SetBlock(Event):
    def __init__(self, block_type:Identifier|str):
        """
        Sets this block to another block type

        :param block_type: The type of block to set
        :type block_type: Identifier | str
        """
        self.block_type = Identifier.parse(block_type)
        
    @property
    def __dict__(self):
        data = {
            'block_type': str(self.block_type)
        }
        return data
    
    @property
    def block_type(self) -> Identifier:
        return getattr(self, '_block_type')
    
    @block_type.setter
    def block_type(self, value:Identifier):
        if not isinstance(value, Identifier): raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        setattr(self, '_block_type', value)
        
@event('set_block_at_pos')
class SetBlockAtPos(Event):
    def __init__(self, block_type:Identifier|str, block_offset:list=[0.0, 0.0, 0.0]):
        """
        Sets a block relative to this block to another block type

        :param block_type: The type of block to set
        :type block_type: Identifier | str
        :param block_offset: The offset from the block's center, defaults to [0.0, 0.0, 0.0]
        :type block_offset: list, optional
        """
        self.block_type = Identifier.parse(block_type)
        self.block_offset = block_offset
        
    @property
    def __dict__(self):
        data = {
            'block_type': str(self.block_type),
            'block_offset': self.block_offset
        }
        return data
    
    @property
    def block_type(self) -> Identifier:
        return getattr(self, '_block_type')
    
    @block_type.setter
    def block_type(self, value:Identifier):
        if not isinstance(value, Identifier): raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        setattr(self, '_block_type', value)
        
    @property
    def block_offset(self) -> list:
        return getattr(self, '_block_offset')
    
    @block_offset.setter
    def block_offset(self, value:list):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_block_offset', value)

@event('spawn_loot')
class SpawnLoot(Event):
    def __init__(self, table:str):
        """
        Spawn loot from block

        :param table: File path, relative to the Behavior Pack's path, to the loot table file
        :type table: str
        """
        self.table = table
        
    @property
    def __dict__(self):
        data = {
            'table': str(self.table)
        }
        return data
    
    @property
    def table(self) -> str:
        return getattr(self, '_table')
    
    @table.setter
    def table(self, value:str):
        setattr(self, '_table', str(value))

@event('swing')
class Swing(Event):
    def __init__(self, target:EventTarget=None):
        """
        Event causes the actor to swing

        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: EventTarget, optional
        """
        Event.__init__(self, target)

    @property
    def __dict__(self):
        data = {}
        return data
        
@event('teleport')
class Teleport(Event):
    def __init__(self, avoid_water:bool=True, destination:list=[0.0, 0.0, 0.0], land_on_block:bool=True, max_range:list=[8.0, 8.0, 8.0], target:EventTarget=None):
        """
        Teleport target randomly around destination point

        :param avoid_water: Determines if the teleport avoids putting the target in water, defaults to True
        :type avoid_water: bool, optional
        :param destination: Origin destination of the teleport, defaults to [0.0, 0.0, 0.0]
        :type destination: list, optional
        :param land_on_block: Determines if the teleport places the target on a block, defaults to True
        :type land_on_block: bool, optional
        :param max_range: Max range the target can teleport relative to the origin destination, defaults to [8.0, 8.0, 8.0]
        :type max_range: list, optional
        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: EventTarget, optional
        """
        self.avoid_water = avoid_water
        self.destination = destination
        self.land_on_block = land_on_block
        self.max_range = max_range
        self.target = target
        
    @property
    def __dict__(self):
        data = {
            'avoid_water': self.avoid_water,
            'destination': self.destination,
            'land_on_block': self.land_on_block,
            'max_range': self.max_range
        }
        if self.target not in [None, EventTarget.SELF]: data['target'] = self.target._value_
        return data
    
    @property
    def avoid_water(self) -> bool:
        return getattr(self, '_avoid_water')
    
    @avoid_water.setter
    def avoid_water(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_avoid_water', value)
    
    @property
    def destination(self) -> list:
        return getattr(self, '_destination')
    
    @destination.setter
    def destination(self, value:list):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_destination', value)

    @property
    def land_on_block(self) -> bool:
        return getattr(self, '_land_on_block')
    
    @land_on_block.setter
    def land_on_block(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_land_on_block', value)

    @property
    def max_range(self) -> list:
        return getattr(self, '_max_range')
    
    @max_range.setter
    def max_range(self, value:list):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_max_range', value)

@event('transform_item')
class TransformiIem(Event):
    def __init__(self, transform:Identifier|str):
        """
        Transforms item into another item

        :param transform: Name of the item it should transform into
        :type transform: Identifier | str
        """
        self.transform = Identifier.parse(transform)
        
    @property
    def __dict__(self):
        data = str(self.transform)
        return data
    
    @property
    def transform(self) -> Identifier:
        return getattr(self, '_transform')
    
    @transform.setter
    def transform(self, value:Identifier):
        if not isinstance(value, Identifier): raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        setattr(self, '_transform', value)

@event('set_block_state')
class SetBlockState(Event):
    def __init__(self, states:dict[str, str]={}, **state:str):
        """
        Sets a block state on this block

        :param states: Block state to set on the block, defaults to {}
        :type states: dict[str, str], optional
        """
        self.states = states
        
    @property
    def __dict__(self):
        data = {}
        for k,v in self.states.items():
            data[str(k)] = str(v)
        return data
    
    @property
    def states(self) -> dict[str, str]:
        return getattr(self, '_states')
    
    @states.setter
    def states(self, value:dict[str, str]):
        if not isinstance(value, dict): raise TypeError(f"Expected dict but got '{value.__class__.__name__}' instead")
        setattr(self, '_states', value)

@event('sequence')
class Sequence(Event):
    def __init__(self):
        """
        Run the same response multiple times, or to only trigger certain aspects of your event when conditions are met.
        """
        self.events = []
        
    @property
    def events(self) -> list[dict]:
        return getattr(self, '_events')
    
    @events.setter
    def events(self, value:list[dict]):
        if not isinstance(value, list): raise TypeError(f"Expected list[Event] but got '{value.__class__.__name__}' instead")
        setattr(self, '_events', value)

    @property
    def __dict__(self):
        data = []
        for v in self.events:
            data.append({})
            if v['condition'] is not None:
                data[-1]['condition'] = str(v['condition'])
            for i, j in v['events'].items():
               data[-1][i.path] = j.__dict__
        return data
    
    # CONDITION

    def set_condition(self, index:int, condition: Molang) -> Molang:
        c = condition if isinstance(condition, Molang) else Molang(condition)
        if not self.event_exists(index): self.events.insert(index, {'events': {}, 'condition': None})
        self.events[index]['condition'] = condition
        return c

    def get_condition(self, index:int) -> Molang:
        return self.events[int(index)]['condition']
    
    def remove_condition(self, index:int) -> Molang:
        e = self.events[int(index)]['condition']
        self.events[int(index)]['condition'] = None
        return e

    # EVENT

    def event_exists(self, index:int) -> bool:
        return (0 <= index) and (index < len(self.events))
    
    def add_event(self, index:int, event:Event) -> Event:
        if not isinstance(event, Event): raise TypeError(f"Expected Event but got '{event.__class__.__name__}' instead")
        if not self.event_exists(index): self.events.insert(index, {'events': {}, 'condition': None})
        self.events[index]['events'][event.id] = event
        return event

    def get_event(self, index:int) -> Event:
        return self.events[int(index)]['events']

    def remove_event(self, index:int) -> Event:
        e = self.events[int(index)]
        del self.events[int(index)]
        return e

    def clear_events(self) -> Self:
        self.events = []
        return self
        
@event('randomize')
class Randomize(Sequence):
    """
    Randomly run event responses
    """
    pass
    
@event('trigger')
class Trigger(Event):
    def __init__(self, event:Identifier|str, condition:Molang=None, target:str=None):
        """
        Trigger an event on a specified target

        :param event: The event to trigger if conditions are met
        :type event: Identifier | str
        :param condition: The conditions to test, defaults to None
        :type condition: Molang, optional
        :param target: The target context to execute against, defaults to EventTarget.SELF
        :type target: str, optional
        """
        Event.__init__(self, target)
        self.event = event
        self.condition = None if condition is None else Molang.parse(condition)
        self.target = target

    @property
    def __dict__(self) -> dict:
        data = {
            'event': str(self.event)
        }
        if self.target not in [None, EventTarget.SELF]:
            data['target'] = self.target._value_
        if self.condition:
            data['condition'] = str(self.condition)
        return data
    
    @property
    def condition(self) -> Molang:
        return getattr(self, '_condition')
    
    @condition.setter
    def condition(self, value:Molang):
        if value is None: setattr(self, '_condition', None)
        elif isinstance(value, Molang): setattr(self, '_condition', value)
        else: raise TypeError(f"Expected Molang but got '{value.__class__.__name__}' instead")

    @property
    def event(self) -> Identifier:
        return getattr(self, '_event')
    
    @event.setter
    def event(self, value:Identifier|str):
        if isinstance(value, (Identifier, str)):
            setattr(self, '_event', Identifier(value))
        else:
            raise TypeError(f"Expected Molang but got '{value.__class__.__name__}' instead")

# CUSTOM

class IncrementBlockState(SetBlockState):
    def __init__(self, name:Identifier, amount:int=1):
        """
        Increase a block state on this block

        :param name: Block state to increase on the block
        :type name: Identifier
        :param amount: The amount to increase, defaults to 1
        :type amount: int, optional
        """
        id = Identifier(name)
        SetBlockState.__init__(self, {id: f"q.block_state('{id}')+{amount}"})

class DecrementBlockState(SetBlockState):
    def __init__(self, name:Identifier, amount:int=1):
        """
        Decrease a block state on this block

        :param name: Block state to decrease on the block
        :type name: Identifier
        :param amount: The amount to decrease, defaults to 1
        :type amount: int, optional
        """
        id = Identifier(name)
        SetBlockState.__init__(self, {id: f"q.block_state('{id}')-{amount}"})

class SwitchBlockState(SetBlockState):
    def __init__(self, name:Identifier):
        """
        Switch a boolean block state on this block. (true = false, false = true)

        :param name: Block state to decrease on the block
        :type name: Identifier
        """
        id = Identifier(name)
        SetBlockState.__init__(self, {id: f"!q.block_state('{id}')"})

