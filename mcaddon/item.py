from typing import Self
import json

from .constant import Category
from .util import Saveable, Identifier, MenuCategory
from .event import Event

# __all__ = ['ItemComponent', 'component', 'MenuCategory', 'ItemEvent', 'Item']

class ItemComponent:
    @property
    def __dict__(self) -> dict:
        raise NotImplementedError()
    
    def json(self) -> str:
        return json.dumps(self.__dict__)

    @classmethod
    def from_dict(cls, data:dict) -> Self:
        raise NotImplementedError()

COMPONENTS:dict[str, ItemComponent] = {}
def component(cls):
    def wrapper():
        global COMPONENTS
        COMPONENTS[cls.id] = cls
        return cls
    return wrapper()

# Components

@component
class AllowOffHandComponent(ItemComponent):
    id = Identifier('allow_off_hand')
    def __init__(self, value:bool):
        self.value = value

    @property
    def __dict__(self) -> bool:
        data = self.value
        return data
    
    @property
    def value(self) -> bool:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:bool):
        if isinstance(value, bool):
            setattr(self, '_value', value)
        else:
            raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")

@component
class BlockPlacerComponent(ItemComponent):
    id = Identifier('block_placer')
    def __init__(self, block:Identifier|str, use_on:list):
        self.block = Identifier.parse(block)
        self.use_on = use_on

    @property
    def __dict__(self) -> dict:
        data = {
            'block': self.block,
            'use_on': self.use_on
        }
        return data
    
    @property
    def block(self) -> Identifier:
        return getattr(self, '_block')
    
    @block.setter
    def block(self, value:Identifier):
        if not isinstance(value, Identifier): raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        setattr(self, '_block', value)

    @property
    def use_on(self) -> list:
        return getattr(self, '_use_on')
    
    @use_on.setter
    def use_on(self, value:list):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_use_on', value)
    
@component
class CanDestroyInCreativeComponent(ItemComponent):
    id = Identifier('can_destroy_in_creative')
    def __init__(self, value:bool):
        self.value = value

    @property
    def __dict__(self) -> bool:
        data = self.value
        return data
    
    @property
    def value(self) -> bool:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)
    
@component
class CooldownComponent(ItemComponent):
    id = Identifier('cooldown')
    def __init__(self, category:str, duration:float):
        self.category = category
        self.duration = duration
        
    @property
    def __dict__(self) -> dict:
        data = {
            'category': self.category,
            'duration': self.duration
        }
        return data
    
    @property
    def category(self) -> str:
        return getattr(self, '_category')
    
    @category.setter
    def category(self, value:str):
        setattr(self, '_category', str(value))

    @property
    def duration(self) -> float:
        return getattr(self, '_duration')
    
    @duration.setter
    def duration(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_duration', value)
    
@component
class DamageComponent(ItemComponent):
    id = Identifier('damage')
    def __init__(self, value:int):
        self.value = value
        
    @property
    def __dict__(self) -> dict:
        data = {
            'value': self.value
        }
        return data
    
    @property
    def value(self) -> int:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:int):
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)
    
@component
class DisplayNameComponent(ItemComponent):
    id = Identifier('display_name')
    def __init__(self, value:str):
        self.value = value
        
    @property
    def __dict__(self) -> dict:
        data = {
            'value': self.value
        }
        return data
    
    @property
    def value(self) -> str:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:str):
        setattr(self, '_value', str(value))
    
@component
class DurabilityComponent(ItemComponent):
    id = Identifier('durability')
    def __init__(self, damage_chance:float, max_durability:int):
        self.damage_chance = damage_chance
        self.max_durability = max_durability
        
    @property
    def __dict__(self) -> dict:
        data = {
            'damage_chance': self.damage_chance,
            'max_durability': self.max_durability
        }
        return data
    
    @property
    def damage_chance(self) -> float:
        return getattr(self, '_damage_chance')
    
    @damage_chance.setter
    def damage_chance(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_damage_chance', value)
    
    @property
    def max_durability(self) -> int:
        return getattr(self, '_max_durability')
    
    @max_durability.setter
    def max_durability(self, value:int):
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_max_durability', value)

@component
class EnchantableComponent(ItemComponent):
    id = Identifier('enchantable')
    def __init__(self, slot:str, value:int):
        self.slot = slot
        self.value = value
        
    @property
    def __dict__(self) -> dict:
        data = {
            'slot': self.slot,
            'value': self.value
        }
        return data
    
    @property
    def slot(self) -> str:
        return getattr(self, '_slot')
    
    @slot.setter
    def slot(self, value:str):
        setattr(self, '_slot', str(value))

    @property
    def value(self) -> int:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:int):
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)
    
@component
class EntityPlacerComponent(ItemComponent):
    id = Identifier('entity_placer')
    def __init__(self, entity:Identifier|str, dispense_on:list, use_on:list):
        self.entity = Identifier.parse(entity)
        self.dispense_on = dispense_on
        self.use_on = use_on
        
    @property
    def __dict__(self) -> dict:
        data = {
            'entity': self.entity,
            'dispense_on': self.dispense_on,
            'use_on': self.use_on
        }
        return data
    
    @property
    def entity(self) -> Identifier:
        return getattr(self, '_entity')
    
    @entity.setter
    def entity(self, value:Identifier):
        if not isinstance(value, Identifier): raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        setattr(self, '_entity', value)

    @property
    def dispense_on(self) -> list:
        return getattr(self, '_dispense_on')
    
    @dispense_on.setter
    def dispense_on(self, value:list):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_dispense_on', value)

    @property
    def use_on(self) -> list:
        return getattr(self, '_use_on')
    
    @use_on.setter
    def use_on(self, value:list):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_use_on', value)

@component
class FoodComponent(ItemComponent):
    id = Identifier('food')
    def __init__(self, nutrition:int, saturation_modifier:float, can_always_eat:bool=False, using_converts_to:Identifier|str=None):
        self.nutrition =nutrition
        self.saturation_modifier = saturation_modifier
        self.can_always_eat = can_always_eat
        self.using_converts_to = using_converts_to
        
    @property
    def __dict__(self) -> dict:
        data = {}
        if self.nutrition is not None: data['nutrution'] = self.nutrition
        if self.saturation_modifier is not None: data['saturation_modifier'] = self.saturation_modifier
        if self.can_always_eat is not False: data['can_always_eat'] = self.can_always_eat
        if self.using_converts_to is not None: data['using_converts_to'] = str(self.using_converts_to)
        return data
    
    @property
    def nutrition(self) -> int:
        return getattr(self, '_nutrition')
    
    @nutrition.setter
    def nutrition(self, value:int):
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_nutrition', value)

    @property
    def saturation_modifier(self) -> float:
        return getattr(self, '_saturation_modifier')
    
    @saturation_modifier.setter
    def saturation_modifier(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_saturation_modifier', value)

    @property
    def can_always_eat(self) -> bool:
        return getattr(self, '_can_always_eat', False)
    
    @can_always_eat.setter
    def can_always_eat(self, value:bool):
        if value is None: value = False
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_can_always_eat', value)

    @property
    def using_converts_to(self) -> Identifier|None:
        return getattr(self, '_using_converts_to', None)
    
    @using_converts_to.setter
    def using_converts_to(self, value:Identifier|None):
        if value is None: setattr(self, '_using_converts_to', None)
        else: setattr(self, '_using_converts_to', Identifier(value))

@component
class FuelComponent(ItemComponent):
    id = Identifier('fuel')
    def __init__(self, duration:float):
        self.duration = duration
        
    @property
    def __dict__(self) -> dict:
        data = {
            'duration': self.duration
        }
        return data
    
    @property
    def duration(self) -> float:
        return getattr(self, '_duration')
    
    @duration.setter
    def duration(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_duration', value)
    
@component
class GlintComponent(ItemComponent):
    id = Identifier('glint')
    def __init__(self, value:bool):
        self.value = value
        
    @property
    def __dict__(self) -> dict:
        data = {
            'value': self.value
        }
        return data
    
    @property
    def value(self) -> bool:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)

@component
class HandEquippedComponent(ItemComponent):
    id = Identifier('hand_equipped')
    def __init__(self, value:bool):
        self.value = value
        
    @property
    def __dict__(self) -> bool:
        data = self.value
        return data
    
    @property
    def value(self) -> bool:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)
    
@component
class HoverTextColorComponent(ItemComponent):
    id = Identifier('hover_text_color')
    def __init__(self, value:str):
        self.value = value
        
    @property
    def __dict__(self) -> dict:
        data = {
            'value': self.value
        }
        return data
    
    @property
    def value(self) -> str:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:str):
        setattr(self, '_value', str(value))
    
@component
class IconComponent(ItemComponent):
    id = Identifier('icon')
    def __init__(self, texture:Identifier|str):
        self.texture = texture
        
    @property
    def __dict__(self) -> dict:
        data = {
            'texture': str(self.texture)
        }
        return data
    
    @property
    def texture(self) -> Identifier:
        return getattr(self, '_texture')
    
    @texture.setter
    def texture(self, value:Identifier|str):
        setattr(self, '_texture', Identifier(value))
    
@component
class InteractButtonComponent(ItemComponent):
    id = Identifier('interact_button')
    def __init__(self, value:str|bool):
        self.value = value
        
    @property
    def __dict__(self) -> dict:
        data = {
            'value': self.value
        }
        return data
    
    @property
    def value(self) -> str:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:str):
        setattr(self, '_value', str(value))
    
@component
class ItemStorageComponent(ItemComponent):
    id = Identifier('item_storage')
    def __init__(self, capacity:int):
        self.capacity = capacity
        
    @property
    def __dict__(self) -> dict:
        data = {
            'capacity': self.capacity
        }
        return data
    
    @property
    def capacity(self) -> int:
        return getattr(self, '_capacity')
    
    @capacity.setter
    def capacity(self, value:int):
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_capacity', value)
    
@component
class LiquidClippedComponent(ItemComponent):
    id = Identifier('liquid_clipped')
    def __init__(self, value:bool):
        self.value = value
        
    @property
    def __dict__(self) -> dict:
        data = {
            'value': self.value
        }
        return data
    
    @property
    def value(self) -> bool:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)
    
@component
class MaxStackSizeComponent(ItemComponent):
    id = Identifier('max_stack_size')
    def __init__(self, value:int):
        self.value = value
        
    @property
    def __dict__(self) -> int:
        data = self.value
        return data
    
    @property
    def value(self) -> int:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:int):
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)
    
@component
class ProjectileComponent(ItemComponent):
    id = Identifier('projectile')
    def __init__(self, projectile_entity:Identifier|str, minimum_critical_power:float):
        self.projectile_entity = Identifier.parse(projectile_entity)
        self.minimum_critical_power = minimum_critical_power
        
    @property
    def __dict__(self) -> dict:
        data = {
            'projectile_entity': self.projectile_entity,
            'minimum_critical_power': self.minimum_critical_power
        }
        return data
    
    @property
    def projectile_entity(self) -> Identifier:
        return getattr(self, '_projectile_entity')
    
    @projectile_entity.setter
    def projectile_entity(self, value:Identifier):
        if not isinstance(value, Identifier): raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        setattr(self, '_projectile_entity', value)

    @property
    def minimum_critical_power(self) -> float:
        return getattr(self, '_minimum_critical_power')
    
    @minimum_critical_power.setter
    def minimum_critical_power(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_minimum_critical_power', value)
    
@component
class RecordComponent(ItemComponent):
    id = Identifier('record')
    def __init__(self, comparator_signal:int, duration:float, sound_event:Identifier|str):
        self.comparator_signal = comparator_signal
        self.duration = duration
        self.sound_event = Identifier.parse(sound_event)
        
    @property
    def __dict__(self) -> dict:
        data = {
            'comparator': self.comparator_signal,
            'duration': self.duration,
            'sound_event': self.sound_event
        }
        return data
    
    @property
    def comparator_signal(self) -> int:
        return getattr(self, '_comparator_signal')
    
    @comparator_signal.setter
    def comparator_signal(self, value:int):
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_comparator_signal', value)

    @property
    def duration(self) -> float:
        return getattr(self, '_duration')
    
    @duration.setter
    def duration(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_duration', value)

    @property
    def sound_event(self) -> Identifier:
        return getattr(self, '_sound_event')
    
    @sound_event.setter
    def sound_event(self, value:Identifier):
        if not isinstance(value, Identifier): raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        setattr(self, '_sound_event', value)
    
class RepairItem:
    pass

@component
class RepairableComponent(ItemComponent):
    id = Identifier('repairable')
    def __init__(self, repair_items:list[RepairItem]):
        self.repair_items = repair_items
        
    @property
    def __dict__(self) -> dict:
        data = {
            'repair_items': []
        }
        for i in self.repair_items:
            data['repair_items'].append(i.__dict__)
        return data
    
    @property
    def repair_items(self) -> list[RepairItem]:
        return getattr(self, '_repair_items')
    
    @repair_items.setter
    def repair_items(self, value:list[RepairItem]):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_repair_items', value)
    
@component
class ShooterComponent(ItemComponent):
    id = Identifier('shooter')
    def __init__(self, ammunition:Identifier|str, charge_on_draw:bool, max_draw_duration:float, scale_power_by_draw_duration:bool):
        self.ammunition = Identifier.parse(ammunition)
        self.charge_on_draw = charge_on_draw
        self.max_draw_duration = max_draw_duration
        self.scale_power_by_draw_duration = scale_power_by_draw_duration
        
    @property
    def __dict__(self) -> dict:
        data = {
            'ammunition': self.ammunition,
            'charge_on_draw': self.charge_on_draw,
            'max_draw_duration': self.max_draw_duration,
            'scale_power_by_draw_duration': self.scale_power_by_draw_duration
        }
        return data
    
    @property
    def ammunition(self) -> Identifier:
        return getattr(self, '_ammunition')
    
    @ammunition.setter
    def ammunition(self, value:Identifier):
        if not isinstance(value, Identifier): raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        setattr(self, '_ammunition', value)

    @property
    def charge_on_draw(self) -> bool:
        return getattr(self, '_charge_on_draw')
    
    @charge_on_draw.setter
    def charge_on_draw(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_charge_on_draw', value)

    @property
    def max_draw_duration(self) -> float:
        return getattr(self, '_max_draw_duration')
    
    @max_draw_duration.setter
    def max_draw_duration(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_max_draw_duration', value)

    @property
    def scale_power_by_draw_duration(self) -> bool:
        return getattr(self, '_scale_power_by_draw_duration')
    
    @scale_power_by_draw_duration.setter
    def scale_power_by_draw_duration(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_scale_power_by_draw_duration', value)
    
@component
class ShouldDespawnComponent(ItemComponent):
    id = Identifier('should_despawn')
    def __init__(self, value:bool):
        self.value = value
        
    @property
    def __dict__(self) -> dict:
        data = {
            'value': self.value
        }
        return data
    
    @property
    def value(self) -> bool:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)

@component
class StackedByDataComponent(ItemComponent):
    id = Identifier('stacked_by_data')
    def __init__(self, value:bool):
        self.value = value
        
    @property
    def __dict__(self) -> dict:
        data = {
            'value': self.value
        }
        return data
    
    @property
    def value(self) -> bool:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)
    
@component
class TagsComponent(ItemComponent):
    id = Identifier('tags')
    def __init__(self, tags:list[Identifier|str]):
        self.tags = tags
        
    @property
    def __dict__(self) -> dict:
        data = {
            'tags': []
        }
        for x in self.tags:
            data['tags'].append(str(x))
        return data
    
    @property
    def tags(self) -> list[Identifier|str]:
        return getattr(self, '_tags')
    
    @tags.setter
    def tags(self, value:list[Identifier|str]):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_tags', value)
    
@component
class ThrowableComponent(ItemComponent):
    id = Identifier('throwable')
    def __init__(self, do_swing_animation:bool, launch_power_scale:bool, max_draw_duration:float, max_launch_power:float, min_draw_duration:float, scale_power_by_draw_duration:bool):
        self.do_swing_animation = do_swing_animation
        self.launch_power_scale = launch_power_scale
        self.max_draw_duration = max_draw_duration
        self.max_launch_power = max_launch_power
        self.min_draw_duration = min_draw_duration
        self.scale_power_by_draw_duration = scale_power_by_draw_duration
        
    @property
    def __dict__(self) -> dict:
        data = {
            'do_swing_animation': self.do_swing_animation,
            'launch_power_scale': self.launch_power_scale,
            'max_draw_duration': self.max_draw_duration,
            'max_launch_power': self.max_draw_duration,
            'min_draw_duration': self.min_draw_duration,
            'scale_power_by_draw_duration': self.scale_power_by_draw_duration
        }
        return data
    
    @property
    def do_swing_animation(self) -> bool:
        return getattr(self, '_do_swing_animation')
    
    @do_swing_animation.setter
    def do_swing_animation(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_do_swing_animation', value)

    @property
    def launch_power_scale(self) -> bool:
        return getattr(self, '_launch_power_scale')
    
    @launch_power_scale.setter
    def launch_power_scale(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_launch_power_scale', value)
    
    @property
    def max_draw_duration(self) -> float:
        return getattr(self, '_max_draw_duration')
    
    @max_draw_duration.setter
    def max_draw_duration(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_max_draw_duration', value)
    
    @property
    def max_launch_power(self) -> float:
        return getattr(self, '_max_launch_power')
    
    @max_launch_power.setter
    def max_launch_power(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_max_launch_power', value)

    @property
    def min_draw_duration(self) -> float:
        return getattr(self, '_min_draw_duration')
    
    @min_draw_duration.setter
    def min_draw_duration(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_min_draw_duration', value)

    @property
    def scale_power_by_draw_duration(self) -> bool:
        return getattr(self, '_scale_power_by_draw_duration')
    
    @scale_power_by_draw_duration.setter
    def scale_power_by_draw_duration(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_scale_power_by_draw_duration', value)

@component
class UseAnimationComponent(ItemComponent):
    id = Identifier('use_animation')
    def __init__(self, value:str):
        self.value = value
        
    @property
    def __dict__(self) -> str:
        data = self.value
        return data
    
    @property
    def value(self) -> str:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:str):
        setattr(self, '_value', str(value))
    
@component
class UseModifiersComponent(ItemComponent):
    id = Identifier('use_modifiers')
    def __init__(self, movement_modifier:float, use_duration:float):
        self.movement_modifier = movement_modifier
        self.use_duration = use_duration
        
    @property
    def __dict__(self) -> dict:
        data = {
            'movement_modifier': self.movement_modifier,
            'use_duration': self.use_duration
        }
        return data
    
    @property
    def movement_modifier(self) -> float:
        return getattr(self, '_movement_modifier')
    
    @movement_modifier.setter
    def movement_modifier(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_movement_modifier', value)

    @property
    def use_duration(self) -> float:
        return getattr(self, '_use_duration')
    
    @use_duration.setter
    def use_duration(self, value:float):
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_use_duration', value)

@component
class WearableComponent(ItemComponent):
    id = Identifier('wearable')
    def __init__(self, protection:int, slot:int):
        self.protection = protection
        self.slot = slot
        
    @property
    def __dict__(self) -> dict:
        data = {
            'protection': self.protection,
            'slot': self.slot
        }
        return data
    
    @property
    def protection(self) -> int:
        return getattr(self, '_protection')
    
    @protection.setter
    def protection(self, value:int):
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_protection', value)

    @property
    def slot(self) -> int:
        return getattr(self, '_slot')
    
    @slot.setter
    def slot(self, value:int):
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_slot', value)
    
@component
class WearableComponent(ItemComponent):
    id = Identifier('digger')
    def __init__(self, destroy_speeds:list, use_efficiency:bool):
        self.destroy_speeds = destroy_speeds
        self.use_efficiency = use_efficiency
        
    @property
    def __dict__(self) -> dict:
        data = {
            'destory_speeds': self.destroy_speeds,
            'use_efficiency': self.use_efficiency
        }
        return data
    
    @property
    def destroy_speeds(self) -> list:
        return getattr(self, '_destroy_speeds')
    
    @destroy_speeds.setter
    def destroy_speeds(self, value:list):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_destroy_speeds', value)

    @property
    def use_efficiency(self) -> bool:
        return getattr(self, '_use_efficiency')
    
    @use_efficiency.setter
    def use_efficiency(self, value:bool):
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_use_efficiency', value)
    
class Item(Saveable):
    format_version = '1.20.51'
    id = Identifier('item')
    def __init__(self, identifier:Identifier|str, menu_category:MenuCategory=None):
        self.identifier = Identifier.parse(identifier)
        self.menu_category = menu_category
        self.components:dict[str, ItemComponent] = {}
        self.events:dict[Identifier, Event] = {}

    @property
    def __dict__(self) -> dict:
        item = {
            'description': {
                'identifier': str(self.identifier)
            }
        }
        if self.menu_category:
            item['description']['menu_category'] = self.menu_category.__dict__

        if self.components:
            item['components'] = {}
            for k,v in self.components.items():
                item['components'][str(k)] = v.__dict__
                        
        if self.events:
            item['events'] = {}
            for key, events in self.events.items():
                d = {}
                for k,v in events.items(): d[k.path] = v.__dict__
                item['events'][str(key)] = d

        data = {
            'format_version': self.format_version,
            str(self.id): item
        }
        return data
    
    @property
    def identifier(self) -> Identifier:
        return getattr(self, '_identifier')
    
    @identifier.setter
    def identifier(self, value:Identifier):
        if not isinstance(value, Identifier): raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        setattr(self, '_identifier', Identifier(value))

    @property
    def menu_category(self) -> MenuCategory:
        return getattr(self, '_menu_category')
    
    @menu_category.setter
    def menu_category(self, value:MenuCategory):
        if value is None:
            setattr(self, '_menu_category', None)
            return None
        if not isinstance(value, MenuCategory): raise TypeError(f"Expected MenuCategory but got '{value.__class__.__name__}' instead")
        setattr(self, '_menu_category', value)

    @property
    def components(self) -> dict[str, ItemComponent]:
        return getattr(self, '_components')
    
    @components.setter
    def components(self, value:dict[str, ItemComponent]):
        if not isinstance(value, dict): raise TypeError(f"Expected dict but got '{value.__class__.__name__}' instead")
        setattr(self, '_components', value)

    @property
    def events(self) -> dict[Identifier, Event]:
        return getattr(self, '_events')
    
    @events.setter
    def events(self, value:dict[Identifier, Event]):
        if not isinstance(value, dict): raise TypeError(f"Expected dict but got '{value.__class__.__name__}' instead")
        setattr(self, '_events', value)

    @classmethod
    def from_dict(cls, data:dict) -> Self:
        self = cls.__new__(cls)
        if str(self.id) in data:
            item = data['minecraft:item']
            if 'description' in item:
                desc = item['description']
                if 'identifier' in desc:
                    self.identifier = desc['identifier']
                    
            if 'components' in item:
                comp = item['components']
                    
            if 'events' in item:
                events = item['events']
        return self

    # COMPONENT

    def add_component(self, component:ItemComponent) -> ItemComponent:
        if not isinstance(component, ItemComponent): raise TypeError(f"Expected ItemComponent but got '{component.__class__.__name__}' instead")
        self.components[component.id] = component
        return component

    def get_component(self, id:str) -> ItemComponent:
        x = id.id if isinstance(id, ItemComponent) else id
        return self.components.get(x)
    
    def remove_component(self, id:str) -> ItemComponent:
        x = id.id if isinstance(id, ItemComponent) else id
        return self.components.pop(x)

    def clear_components(self) -> Self:
        self.components.clear()
        return self
    
    # EVENT

    def add_event(self, id:Identifier|str, event:Event) -> Event:
        if not isinstance(event, Event): raise TypeError(f"Expected ItemEvent but got '{event.__class__.__name__}' instead")
        i = Identifier.parse(id)
        if i in self.events:
            self.events[i][event.id] = event
            return event
        obj = {}
        obj[event.id] = event
        self.events[i] = obj
        event.id
        return event

    def get_event(self, id:Identifier|str) -> Event:
        i = Identifier.parse(id)
        return self.events.get(i)

    def remove_event(self, id:Identifier|str) -> Event:
        i = Identifier.parse(id)
        return self.events.pop(i)

    def clear_events(self) -> Self:
        self.events.clear()
        return self

# VANILLA

class AppleItem(Item):
    def __init__(self, id:Identifier|str):
        Item.__init__(self, id, MenuCategory(Category.ITEMS, 'itemGroup.name.food'))
        self.add_component(FoodComponent(0, 1.0))
        self.add_component(IconComponent('minecraft:apple'))