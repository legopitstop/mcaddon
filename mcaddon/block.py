from typing import Self

from .constant import RenderMethod, BlockFace, Category
from .util import Saveable, Identifier, Molang, MenuCategory
from .event import *

class BlockComponent:
    def __init__(self):
        """
        Base component class for blocks
        """
        ...

    @classmethod
    def from_dict(cls, data:dict) -> Self:
        raise NotImplementedError()
 
# COMPONENTS

COMPONENTS:dict[str, BlockComponent] = {}
def component(cls):
    """
    Add this component to the parser
    """
    def wrapper():
        global COMPONENTS
        COMPONENTS[cls.id] = cls
        return cls
    return wrapper()

# Trigger Components

@component
class OnFallOnComponent(Trigger, BlockComponent):
    id = Identifier('on_fall_on')
    def __init__(self, event:str='on_fall_on', min_fall_distance:float=0.0, condition:str=None, target:str=None):
        """
        Describes event for this block

        :param event: The event executed on the block, defaults to 'on_fall_on'
        :type event: str, optional
        :param min_fall_distance: The minimum distance in blocks that an actor needs to fall to trigger this event, defaults to 0.0
        :type min_fall_distance: float, optional
        :param condition: The condition of event to be executed on the block, defaults to None
        :type condition: str, optional
        :param target: The target of event executed on the block, defaults to None
        :type target: str, optional
        """
        Trigger.__init__(self, event, condition, target)
        self.min_fall_distance = min_fall_distance

    @property
    def __dict__(self):
        data = super().__dict__
        if self.min_fall_distance is not None: data['min_fall_distance'] = self.min_fall_distance
        return data
    
    @property
    def min_fall_distance(self) -> float:
        return getattr(self, '_min_fall_distance', None)
    
    @min_fall_distance.setter
    def min_fall_distance(self, value:float):
        if value is None:
            setattr(self, '_min_fall_distance', None)
            return
        setattr(self, '_min_fall_distance', float(value))

@component
class OnInteractComponent(Trigger, BlockComponent):
    id = Identifier('on_interact')
    def __init__(self, event:str='on_interact', condition:str=None, target:str=None):
        """
        Describes event for this block

        :param event: The event executed on the block, defaults to 'on_fall_on'
        :type event: str, optional
        :param min_fall_distance: The minimum distance in blocks that an actor needs to fall to trigger this event, defaults to 0.0
        :type min_fall_distance: float, optional
        :param condition: The condition of event to be executed on the block, defaults to None
        :type condition: str, optional
        :param target: The target of event executed on the block, defaults to None
        :type target: str, optional
        """
        Trigger.__init__(self, event, condition, target)

@component
class OnPlacedComponent(Trigger, BlockComponent):
    id = Identifier('on_placed')
    def __init__(self, event:str='on_placed', condition:str=None, target:str=None):
        """
        Describes event for this block

        :param event: The event executed on the block, defaults to 'on_fall_on'
        :type event: str, optional
        :param min_fall_distance: The minimum distance in blocks that an actor needs to fall to trigger this event, defaults to 0.0
        :type min_fall_distance: float, optional
        :param condition: The condition of event to be executed on the block, defaults to None
        :type condition: str, optional
        :param target: The target of event executed on the block, defaults to None
        :type target: str, optional
        """
        Trigger.__init__(self, event, condition, target)

@component
class OnPlayerDestroyedComponent(Trigger, BlockComponent):
    id = Identifier('on_player_destoryed')
    def __init__(self, event:str='on_player_destoryed', condition:str=None, target:str=None):
        """
        Describes event for this block

        :param event: The event executed on the block, defaults to 'on_fall_on'
        :type event: str, optional
        :param min_fall_distance: The minimum distance in blocks that an actor needs to fall to trigger this event, defaults to 0.0
        :type min_fall_distance: float, optional
        :param condition: The condition of event to be executed on the block, defaults to None
        :type condition: str, optional
        :param target: The target of event executed on the block, defaults to None
        :type target: str, optional
        """
        Trigger.__init__(self, event, condition, target)

@component
class OnPlayerPlacingComponent(Trigger, BlockComponent):
    id = Identifier('on_player_placing')
    def __init__(self, event:str='on_player_placing', condition:str=None, target:str=None):
        """
        Describes event for this block

        :param event: The event executed on the block, defaults to 'on_fall_on'
        :type event: str, optional
        :param min_fall_distance: The minimum distance in blocks that an actor needs to fall to trigger this event, defaults to 0.0
        :type min_fall_distance: float, optional
        :param condition: The condition of event to be executed on the block, defaults to None
        :type condition: str, optional
        :param target: The target of event executed on the block, defaults to None
        :type target: str, optional
        """
        Trigger.__init__(self, event, condition, target)

@component
class OnStepOffComponent(Trigger, BlockComponent):
    id = Identifier('on_step_off')
    def __init__(self, event:str='on_step_off', condition:str=None, target:str=None):
        """
        Describes event for this block

        :param event: The event executed on the block, defaults to 'on_fall_on'
        :type event: str, optional
        :param min_fall_distance: The minimum distance in blocks that an actor needs to fall to trigger this event, defaults to 0.0
        :type min_fall_distance: float, optional
        :param condition: The condition of event to be executed on the block, defaults to None
        :type condition: str, optional
        :param target: The target of event executed on the block, defaults to None
        :type target: str, optional
        """
        Trigger.__init__(self, event, condition, target)

@component
class OnStepOnComponent(Trigger, BlockComponent):
    id = Identifier('on_step_on')
    def __init__(self, event:str='on_step_on', condition:str=None, target:str=None):
        """
        Describes event for this block

        :param event: The event executed on the block, defaults to 'on_fall_on'
        :type event: str, optional
        :param min_fall_distance: The minimum distance in blocks that an actor needs to fall to trigger this event, defaults to 0.0
        :type min_fall_distance: float, optional
        :param condition: The condition of event to be executed on the block, defaults to None
        :type condition: str, optional
        :param target: The target of event executed on the block, defaults to None
        :type target: str, optional
        """
        Trigger.__init__(self, event, condition, target)

@component
class BoneVisabilityComponent(BlockComponent):
    id = Identifier('bone_visability')
    def __init__(self, bones:dict[str, str], **bone):
        """
        Tells whether the bone should be visible or not (value).

        :param bones: A dict that contains a list of key/value pairs that map from bone name in the specified geometry file (key) to a boolean
        :type bones: dict[str, str]
        """
        self.bones = bones

    @property
    def __dict__(self) -> dict:
        data = {
            'bones': self.bones
        }
        return data
    
    @property
    def bones(self) -> dict[str, str]:
        return getattr(self, '_bones')
    
    @bones.setter
    def bones(self, value:dict[str, str]):
        if not isinstance(value, dict): raise TypeError(f"Expected dict[str, str] but got '{value.__class__.__name__}' instead")
        setattr(self, '_bones', value)

@component
class BreathabilityComponent(BlockComponent):
    id = Identifier('breathability')
    def __init__(self, value:str):
        """
        Determines whether the block is breathable by defining if the block is treated as a `solid` or as `air`. The default is `solid` if this component is omitted.

        :param value: `solid` or `air`
        :type value: str
        """
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

# SUBCLASS
class Box(BlockComponent):
    def __init__(self, origin:list|bool=[-8.0, 0, -8.0], size:list=[16.0, 16.0, 16.0]):
        self.origin = origin
        self.size = size

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.origin is not None: data['origin'] = self.origin
        if self.size is not None: data['size'] = self.size
        if isinstance(self.origin, bool): data = self.origin
        return data
    
    @property
    def origin(self) -> list[float]:
        return getattr(self, '_origin', None)
    
    @origin.setter
    def origin(self, value:list[float]):
        if value is None:
            setattr(self, '_origin', None)
            return
        elif isinstance(value, bool):
            setattr(self, '_origin', value)
        elif isinstance(value, list):
            setattr(self, '_origin', value)
        else:
            raise TypeError(f"Expected list[float] but got '{value.__class__.__name__}' instead")

    @property
    def size(self) -> list[float]:
        return getattr(self, '_size', None)
    
    @size.setter
    def size(self, value:list[float]):
        if value is None:
            setattr(self, '_size', None)
            return
        if not isinstance(value, list): raise TypeError(f"Expected list[float] but got '{value.__class__.__name__}' instead")
        setattr(self, '_size', value)

    @classmethod
    def cube(cls) -> Self:
        self = cls.__new__(cls)
        self.origin = [-8, 0, -8]
        self.size = [16, 16, 16]
        return self

    @classmethod
    def none(cls) -> Self:
        self = cls.__new__(cls)
        self.origin = False
        return self

@component
class CollisionBoxComponent(Box):
    id = Identifier('collision_box')
    def __init__(self, origin:list|bool=[-8.0, 0, -8.0], size:list=[16.0, 16.0, 16.0]):
        """
        Defines the area of the block that collides with entities. If set to true, default values are used. If set to false, the block's collision with entities is disabled. If this component is omitted, default values are used.

        :param origin: Minimal position of the bounds of the collision box. "origin" is specified as [x, y, z] and must be in the range (-8, 0, -8) to (8, 16, 8), inclusive, defaults to [-8.0, 0, -8.0]
        :type origin: list | bool, optional
        :param size: Size of each side of the collision box. Size is specified as [x, y, z]. "origin" + "size" must be in the range (-8, 0, -8) to (8, 16, 8), inclusive, defaults to [16.0, 16.0, 16.0]
        :type size: list, optional
        """
        Box.__init__(self, origin, size)

@component
class SelectionBoxComponent(Box):
    id = Identifier('selection_box')
    def __init__(self, origin:list|bool=[-8.0, 0, -8.0], size:list=[16.0, 16.0, 16.0]):
        """
        Defines the area of the block that is selected by the player's cursor. If set to true, default values are used. If set to false, this block is not selectable by the player's cursor. If this component is omitted, default values are used.

        :param origin: Minimal position of the bounds of the collision box. "origin" is specified as [x, y, z] and must be in the range (-8, 0, -8) to (8, 16, 8), inclusive, defaults to [-8.0, 0, -8.0]
        :type origin: list | bool, optional
        :param size: Size of each side of the collision box. Size is specified as [x, y, z]. "origin" + "size" must be in the range (-8, 0, -8) to (8, 16, 8), inclusive, defaults to [16.0, 16.0, 16.0]
        :type size: list, optional
        """
        Box.__init__(self, origin, size)

@component
class CraftingTableComponent(BlockComponent):
    id = Identifier('crafting_table')
    def __init__(self, crafting_tags:list[str], table_name:str):
        """
        Makes your block into a custom crafting table which enables the crafting table UI and the ability to craft recipes. This component supports only "recipe_shaped" and "recipe_shapeless" typed recipes and not others like "recipe_furnace" or "recipe_brewing_mix". If there are two recipes for one item, the recipe book will pick the first that was parsed. If two input recipes are the same, crafting may assert and the resulting item may vary.

        :param crafting_tags: Defines the tags recipes should define to be crafted on this table. Limited to 64 tags. Each tag is limited to 64 characters.
        :type crafting_tags: list[str]
        :param table_name: Specifies the language file key that maps to what text will be displayed in the UI of this table. If the string given can not be resolved as a loc string, the raw string given will be displayed. If this field is omitted, the name displayed will default to the name specified in the "display_name" component. If this block has no "display_name" component, the name displayed will default to the name of the block.
        :type table_name: str
        """
        self.crafting_tags = crafting_tags
        self.table_name = table_name

    @property
    def __dict__(self) -> dict:
        data = {
            'crafting_tags': self.crafting_tags,
            'table_name': self.table_name
        }
        return data
    
    @property
    def crafting_tags(self) -> list[str]:
        return getattr(self, '_crafting_tags')
    
    @crafting_tags.setter
    def crafting_tags(self, value:list[str]):
        if not isinstance(value, list[str]): raise TypeError(f"Expected list[str] but got '{value.__class__.__name__}' instead")
        setattr(self, '_crafting_tags', value)

    @property
    def table_name(self) -> str:
        return getattr(self, '_table_name')
    
    @table_name.setter
    def table_name(self, value:str):
        setattr(self, '_table_name', str(value))

@component
class DestructibleByExplosionComponent(BlockComponent):
    id = Identifier('destructible_by_explosion')
    def __init__(self, explosion_resistance:float=None):
        """
        Describes the destructible by explosion properties for this block. If set to true, the block will have the default explosion resistance. If set to false, this block is indestructible by explosion. If the component is omitted, the block will have the default explosion resistance

        :param explosion_resistance: Sets the explosion resistance for the block. Greater values result in greater resistance to explosions. The scale will be different for different explosion power levels. A negative value or 0 means it will easily explode; larger numbers increase level of resistance, defaults to None
        :type explosion_resistance: float, optional
        """
        self.explosion_resistance = explosion_resistance

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.explosion_resistance is not None: data['explosion_resistance'] = self.explosion_resistance
        return data

    @property
    def explosion_resistance(self) -> float:
        return getattr(self, '_explosion_resistance')
    
    @explosion_resistance.setter
    def explosion_resistance(self, value:float):
        if value is None:
            setattr(self, '_explosion_resistance', value)
            return
        if not isinstance(value, (float, int)): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_explosion_resistance', value)

@component
class DestructibleByMiningComponent(BlockComponent):
    id = Identifier('destructible_by_mining')
    def __init__(self, seconds_to_destory:float=None):
        """
        Describes the destructible by mining properties for this block. If set to true, the block will take the default number of seconds to destroy. If set to false, this block is indestructible by mining. If the component is omitted, the block will take the default number of seconds to destroy.

        :param seconds_to_destory: Sets the number of seconds it takes to destroy the block with base equipment. Greater numbers result in greater mining times, defaults to None
        :type seconds_to_destory: float, optional
        """
        self.seconds_to_destory = seconds_to_destory

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.seconds_to_destory is not None: data['seconds_to_destory'] = self.seconds_to_destory
        return data
    
    @property
    def seconds_to_destory(self) -> float:
        return getattr(self, '_seconds_to_destory')
    
    @seconds_to_destory.setter
    def seconds_to_destory(self, value:float):
        if value is None:
            setattr(self, '_seconds_to_destory', None)
            return        
        if not isinstance(value, (float, int)): raise TypeError(f"Expected float or int but got '{value.__class__.__name__}' instead")
        setattr(self, '_seconds_to_destory', value)

@component
class DisplayNameComponent(BlockComponent):
    id = Identifier('display_name')
    def __init__(self, value:str):
        """
        Specifies the language file key that maps to what text will be displayed when you hover over the block in your inventory and hotbar. If the string given can not be resolved as a loc string, the raw string given will be displayed. If this component is omitted, the name of the block will be used as the display name.
        """
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
class FlammableComponent(BlockComponent):
    id = Identifier('flammable')
    def __init__(self, catch_chance_modifier:int=None, destroy_chance_modifier:int=None):
        """
        Describes the flammable properties for this block. If set to true, default values are used. If set to false, or if this component is omitted, the block will not be able to catch on fire naturally from neighbors, but it can still be directly ignited.

        :param catch_chance_modifier: A modifier affecting the chance that this block will catch flame when next to a fire. Values are greater than or equal to 0, with a higher number meaning more likely to catch on fire. For a "catch_chance_modifier" greater than 0, the fire will continue to burn until the block is destroyed (or it will burn forever if the "destroy_chance_modifier" is 0). If the "catch_chance_modifier" is 0, and the block is directly ignited, the fire will eventually burn out without destroying the block (or it will have a chance to be destroyed if "destroy_chance_modifier" is greater than 0). The default value of 5 is the same as that of Planks, defaults to None
        :type catch_chance_modifier: int, optional
        :param destroy_chance_modifier: A modifier affecting the chance that this block will be destroyed by flames when on fire. Values are greater than or equal to 0, with a higher number meaning more likely to be destroyed by fire. For a "destroy_chance_modifier" of 0, the block will never be destroyed by fire, and the fire will burn forever if the "catch_chance_modifier" is greater than 0. The default value of 20 is the same as that of Planks, defaults to None
        :type destroy_chance_modifier: int, optional
        """
        self.catch_chance_modifier = catch_chance_modifier
        self.destroy_chance_modifier = destroy_chance_modifier

    @property
    def __dict__(self) -> dict:
        data = {}
        if self.catch_chance_modifier is not None: data['catch_chance_modifier'] = self.catch_chance_modifier
        if self.destroy_chance_modifier is not None: data['destroy_chance_modifier'] = self.destroy_chance_modifier
        return data
    
    @property
    def catch_chance_modifier(self) -> int:
        return getattr(self, '_catch_chance_modifier', None)
    
    @catch_chance_modifier.setter
    def catch_chance_modifier(self, value:int):
        if value is None:
            setattr(self, '_catch_chance_modifier', None)
            return
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_catch_chance_modifier', value)

    @property
    def destroy_chance_modifier(self) -> int:
        return getattr(self, '_destroy_chance_modifier', None)
    
    @destroy_chance_modifier.setter
    def destroy_chance_modifier(self, value:int):
        if value is None:
            setattr(self, '_destroy_chance_modifier', None)
            return
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_destroy_chance_modifier', value)

@component
class FrictionComponent(BlockComponent):
    id = Identifier('friction')
    def __init__(self, value:float=None):
        """
        Describes the friction for this block in a range of (0.0-0.9). Friction affects an entity's movement speed when it travels on the block. Greater value results in more friction.
        """
        self.value = value

    @property
    def __dict__(self) -> int:
        data = 0.4 if self.value is None else self.value
        return data
    
    @property
    def value(self) -> float:
        return getattr(self, '_value', None)
    
    @value.setter
    def value(self, value:float):
        if value is None:
            setattr(self, '_value', None)
            return
        if not isinstance(value, float): raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)

@component
class GeometryComponent(BlockComponent):
    id = Identifier('geometry')
    def __init__(self, value:str):
        """
        The description identifier of the geometry file to use to render this block. This identifier must match an existing geometry identifier in any of the currently loaded resource packs.
        """
        self.value = value

    @property
    def __dict__(self):
        data = self.value
        return data
    
    @property
    def value(self) -> str:
        return getattr(self, '_value')
    
    @value.setter
    def value(self, value:str):
        if not value.startswith('geometry.'): value = 'geometry.'+value
        setattr(self, '_value', str(value))

@component
class LightDampeningComponent(BlockComponent):
    id = Identifier('light_dampening')
    def __init__(self, value:int=None):
        """
        The amount that light will be dampened when it passes through the block, in a range (0-15). Higher value means the light will be dampened more.
        """
        self.value = value

    @property
    def __dict__(self) -> int:
        data = 15 if self.value is None else self.value
        return data

    @property
    def value(self) -> int:
        return getattr(self, '_value', None)
    
    @value.setter
    def value(self, value:int):
        if value is None:
            setattr(self, '_value', None)
            return
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)

@component
class LightEmissionComponent(BlockComponent):
    id = Identifier('light_emission')
    def __init__(self, value:int=None):
        """
        The amount of light this block will emit in a range (0-15). Higher value means more light will be emitted
        """
        self.value = value

    @property
    def __dict__(self) -> str:
        data = 0 if self.value is None else self.value
        return data
    
    @property
    def value(self) -> int:
        return getattr(self, '_value', None)
    
    @value.setter
    def value(self, value:int):
        if value is None:
            setattr(self, '_value', None)
            return
        if not isinstance(value, int): raise TypeError(f"Expected int but got '{value.__class__.__name__}' instead")
        setattr(self, '_value', value)

@component
class LootComponent(BlockComponent):
    id = Identifier('loot')
    def __init__(self, value:str):
        """
        The path to the loot table, relative to the behavior pack. Path string is limited to 256 characters
        """
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
class MapColorComponent(BlockComponent):
    id = Identifier('map_color')
    def __init__(self, value:str):
        """
        Sets the color of the block when rendered to a map. The color is represented as a hex value in the format "#RRGGBB". May also be expressed as an array of [R, G, B] from 0 to 255. If this component is omitted, the block will not show up on the map.
        """
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

class Material:
    def __init__(self, texture:Identifier, render_method:RenderMethod=RenderMethod.OPAQUE, ambient_occlusion:bool=True, face_dimming:bool=True):
        """
        A material instance definition to map to a material instance in a geometry file. The material instance "*" will be used for any materials that don't have a match.

        :param texture: Texture name for the material
        :type texture: Identifier
        :param render_method: The render method to use. Must be one of these options:
            "opaque" - Used for a regular block texture without an alpha layer. Does not allow for transparency or translucency.

            "double_sided" - Used for completely disabling backface culling.

            "blend" - Used for a block like stained glass. Allows for transparency and translucency (slightly transparent textures).

            "alpha_test" - Used for a block like the vanilla (unstained) glass. Does not allow for translucency, only fully opaque or fully transparent textures. Also disables backface culling, defaults to RenderMethod.OPAQUE
            
        :type render_method: RenderMethod, optional
        :param ambient_occlusion: Should this material have ambient occlusion applied when lighting? If true, shadows will be created around and underneath the block, defaults to True
        :type ambient_occlusion: bool, optional
        :param face_dimming: Should this material be dimmed by the direction it's facing, defaults to True
        :type face_dimming: bool, optional
        """
        self.texture = texture
        self.ambient_occlusion = ambient_occlusion
        self.face_dimming = face_dimming
        self.render_method = render_method

    @property
    def __dict__(self) -> dict:
        data = {
            'texture': str(self.texture)
        }
        if self.ambient_occlusion not in [None, True]: data['ambient_occlusion'] = self.ambient_occlusion
        if self.face_dimming not in [None, True]: data['face_dimming'] = self.face_dimming
        if self.render_method not in [None, RenderMethod.OPAQUE]: data['render_method'] = self.render_method._value_
        return data
    
    @property
    def texture(self) -> Identifier:
        return getattr(self, '_texture')
    
    @texture.setter
    def texture(self, value:Identifier):
        setattr(self, '_texture', Identifier(value))

    @property
    def ambient_occlusion(self) -> bool:
        return getattr(self, '_ambient_occlusion', None)
    
    @ambient_occlusion.setter
    def ambient_occlusion(self, value:bool):
        if value is None:
            setattr(self, '_ambient_occlusion', None)
            return
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_ambient_occlusion', value)

    @property
    def face_dimming(self) -> bool:
        return getattr(self, '_face_dimming', None)
    
    @face_dimming.setter
    def face_dimming(self, value:bool):
        if value is None:
            setattr(self, '_face_dimming', None)
            return
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_face_dimming', value)

    @property
    def render_method(self) -> RenderMethod:
        return getattr(self, '_render_method', None)
    
    @render_method.setter
    def render_method(self, value:RenderMethod):
        if value is None:
            setattr(self, '_render_method', None)
            return
        if not isinstance(value, RenderMethod): raise TypeError(f"Expected RenderMethod but got '{value.__class__.__name__}' instead")
        setattr(self, '_render_method', value)

@component
class MaterialInstancesComponent(BlockComponent):
    id = Identifier('material_instances')
    def __init__(self):
        """
        The material instances for a block. Maps face or material_instance names in a geometry file to an actual material instance. You can assign a material instance object to any of these faces: "up", "down", "north", "south", "east", "west", or "*". You can also give an instance the name of your choosing such as "my_instance", and then assign it to a face by doing "north":"my_instance".
        """
        self.materials = {}

    @property
    def __dict__(self) -> dict:
        data = {}
        for k,v in self.materials.items():
            data[k] = v.__dict__
        return data
    
    @property
    def materials(self) -> dict[str, Material]:
        return getattr(self, '_materials', {})
    
    @materials.setter
    def materials(self, value:dict[str, Material]):
        if value is None:
            setattr(self, '_materials', {})
            return
        if not isinstance(value, dict): raise TypeError(f"Expected dict[str, Material] but got '{value.__class__.__name__}' instead")
        setattr(self, '_materials', value)
    
    def get_material(self, instance_name:str) -> Material|None:
        return self.materials.get(instance_name)

    def add_material(self, instance_name:str, material:Material) -> Material:
        if not isinstance(material, Material): raise TypeError(f"Expected Material but got '{material.__class__.__name__}' instead")
        self.materials[str(instance_name)] = material
        return material
    
    def remove_material(self, instance_name:str) -> Material:
        m = self.materials[str(instance_name)]
        del self.materials[str(instance_name)]
        return m

class BlockDescriptor:
    def __init__(self, name:str, states:list, tags:str="1"):
        """
        :param name: The name of a block
        :type name: str
        :param states: The list of Vanilla block states and their values that the block can have, expressed in key/value pairs
        :type states: list
        :param tags: A condition using Molang queries that results to true/false that can be used to query for blocks with certain tags, defaults to "1"
        :type tags: str, optional
        """
        self.name = name
        self.states = states
        self.tags = tags

    @property
    def __dict__(self) -> dict:
        data = {
            'name': self.name,
            'states': self.states,
            'tags': self.tags
        }
        return data
    
    @property
    def name(self) -> str:
        return getattr(self, '_name')
    
    @name.setter
    def name(self, value:str):
        setattr(self, '_name', str(value))

    @property
    def states(self) -> list:
        return getattr(self, '_states')
    
    @states.setter
    def states(self, value:list):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_states', value)

    @property
    def tags(self) -> str:
        return getattr(self, '_tags')
    
    @tags.setter
    def tags(self, value:str):
        setattr(self, '_tags', str(value))

class Filter:
    def __init__(self, allowed_faces:list[BlockFace]=[], block_filter:list[BlockDescriptor]=[]):
        """
        condition where the block can be placed/survive

        :param allowed_faces: List of any of the following strings describing which face(s) this block can be placed on: "up", "down", "north", "south", "east", "west", "side", "all". Limited to 6 faces, defaults to []
        :type allowed_faces: list[str], optional
        :param block_filter: List of blocks that this block can be placed against in the "allowed_faces" direction. Limited to 64 blocks. Each block in this list can either be specified as a String (block name) or as a BlockDescriptor. A BlockDescriptor is an object that allows you to reference a block (or multiple blocks) based on its tags, or based on its name and states, defaults to []
        :type block_filter: list[BlockFilter], optional
        """
        self.allowed_faces = allowed_faces
        self.block_filter = block_filter

    @property
    def __dict__(self) -> dict:
        data = {
            'allowed_faces': [x._value_ for x in self.allowed_faces],
            'block_filter': []
        }
        for v in self.block_filter:
            data['block_filter'] = v.__dict__
        return data
    
    @property
    def allowed_faces(self) -> list[BlockFace]:
        return getattr(self, '_allowed_faces', [])
    
    @allowed_faces.setter
    def allowed_faces(self, value:list[BlockFace]):
        if value is None:
            setattr(self, '_allowed_faces', [])
            return
        if not isinstance(value, list): raise TypeError(f"Expected list[BlockFace] but got '{value.__class__.__name__}' instead")
        setattr(self, '_allowed_faces', value)
    
    @property
    def block_filter(self) -> list[BlockDescriptor]:
        return getattr(self, '_block_filter', [])
    
    @block_filter.setter
    def block_filter(self, value:list[BlockDescriptor]):
        if value is None:
            setattr(self, '_block_filter', [])
            return
        if not isinstance(value, list): raise TypeError(f"Expected list[BlockDescriptor] but got '{value.__class__.__name__}' instead")
        setattr(self, '_block_filter', value)

@component
class PlacementFilterComponent(BlockComponent):
    id = Identifier('placement_filter')
    def __init__(self, conditions:list[Filter]=[]):
        """
        Sets rules for under what conditions the block can be placed/survive

        :param conditions: List of conditions where the block can be placed/survive. Limited to 64 conditions, defaults to []
        :type conditions: list[Filter], optional
        """
        self.conditions = conditions
        
    @property
    def __dict__(self) -> dict:
        data = {
            'conditions': []
        }
        for v in self.conditions:
            data['conditions'] = v.__dict__
        return data
    
    @property
    def conditions(self) -> list[Filter]:
        return getattr(self, '_conditions', [])
    
    @conditions.setter
    def conditions(self, value:list[Filter]):
        if value is None:
            setattr(self, '_conditions', [])
            return
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_conditions', value)

@component
class QueuedTickingComponent(BlockComponent):
    id = Identifier('queued_ticking')
    def __init__(self, interval_range:list[int], on_tick:Trigger, looping:bool=None):
        """
        Triggers the specified event, either once, or at a regular interval equal to a number of ticks randomly chosen from the interval_range provided

        :param interval_range: A range of values, specified in ticks, that will be used to decide the interval between times this event triggers. Each interval will be chosen randomly from the range, so the times between this event triggering will differ given an interval_range of two different values. If the values in the interval_range are the same, the event will always be triggered after that number of ticks
        :type interval_range: list[int]
        :param on_tick: The event that will be triggered once or on an interval
        :type on_tick: Trigger
        :param looping: Does the event loop? If false, the event will only be triggered once, after a delay equal to a number of ticks randomly chosen from the interval_range. If true, the event will loop, and each interval between events will be equal to a number of ticks randomly chosen from the interval_range, defaults to None
        :type looping: bool, optional
        """
        self.interval_range = interval_range
        self.on_tick = on_tick
        self.looping = looping
        
    @property
    def __dict__(self) -> dict:
        data = {
            'interval_range': self.interval_range,
            'on_tick': self.on_tick.__dict__
        }
        if self.looping is not None: data['looping'] = self.looping
        return data
    
    @property
    def interval_range(self) -> list[int]:
        return getattr(self, '_interval_range')
    
    @interval_range.setter
    def interval_range(self, value:list[int]):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_interval_range', value)

    @property
    def on_tick(self) -> Trigger:
        return getattr(self, '_on_tick')
    
    @on_tick.setter
    def on_tick(self, value:Trigger):
        if not isinstance(value, Trigger): raise TypeError(f"Expected Trigger but got '{value.__class__.__name__}' instead")
        setattr(self, '_on_tick', value)

    @property
    def looping(self) -> bool:
        return getattr(self, '_looping', None)
    
    @looping.setter
    def looping(self, value:bool):
        if value is None:
            setattr(self, '_looping', None)
            return
        if not isinstance(value, bool): raise TypeError(f"Expected bool but got '{value.__class__.__name__}' instead")
        setattr(self, '_looping', value)

@component
class RandomTickingComponent(BlockComponent):
    id = Identifier('random_ticking')
    def __init__(self, on_tick:Trigger):
        """
        Triggers the specified event randomly based on the random tick speed gamerule. The random tick speed determines how often blocks are updated. Some other examples of game mechanics that use random ticking are crop growth and fire spreading

        :param on_tick: The event that will be triggered on random ticks
        :type on_tick: Trigger
        """
        self.on_tick = on_tick
        
    @property
    def __dict__(self) -> dict:
        data = {
            'on_tick': self.on_tick.__dict__
        }
        return data
    
    @property
    def on_tick(self) -> Trigger:
        return getattr(self, '_on_tick')
    
    @on_tick.setter
    def on_tick(self, value:Trigger):
        if not isinstance(value, Trigger): raise TypeError(f"Expected Trigger but got '{value.__class__.__name__}' instead")
        setattr(self, '_on_tick', value)

@component
class TransformationComponent(BlockComponent):
    id = Identifier('transformation')
    def __init__(self, rotation:list[float]=None, translation:list[float]=None, scale:list[float]=None):
        """
        The block's translation, rotation and scale with respect to the center of its world position

        :param rotation: The rotation of the block, defaults to None
        :type rotation: list[float], optional
        :param translation: The translation of the block, defaults to None
        :type translation: list[float], optional
        :param scale: The scale of the block, defaults to None
        :type scale: list[float], optional
        """
        self.rotation = rotation
        self.translation = translation
        self.scale = scale
        
    @property
    def __dict__(self) -> dict:
        data = {}
        if self.rotation is not None: data['rotation'] = self.rotation
        if self.translation is not None: data['translation'] = self.translation
        if self.scale is not None: data['scale'] = self.scale
        return data
    
    @property
    def rotation(self) -> list[float]:
        return getattr(self, '_rotation', None)
    
    @rotation.setter
    def rotation(self, value:list[float]):
        if value is None:
            setattr(self, '_rotation', None)
            return
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_rotation', value)

    @property
    def translation(self) -> list[float]:
        return getattr(self, '_translation', None)
    
    @translation.setter
    def translation(self, value:list[float]):
        if value is None:
            setattr(self, '_translation', None)
            return
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_translation', value)

    @property
    def scale(self) -> list[float]:
        return getattr(self, '_scale', None)
    
    @scale.setter
    def scale(self, value:list[float]):
        if value is None:
            setattr(self, '_scale', None)
            return
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_scale', value)
        
@component
class UnitCubeComponent(BlockComponent):
    id = Identifier('unit_cube')
    def __init__(self):
        """
        Specifies that a unit cube is to be used with tessellation.
        """
        ...
        
    @property
    def __dict__(self) -> dict:
        return {}

@component
class BlockTags(BlockComponent):
    id = Identifier('tags')
    def __init__(self, tags:list[Identifier]):
        """
        Specifies that a unit cube is to be used with tessellation.
        """
        self.tags = tags

    @property
    def __dict__(self) -> dict:
        return [str(x) for x in self.tags]
    
    @property
    def tags(self) -> list[Identifier]:
        return getattr(self, '_tags')
    
    @tags.setter
    def tags(self, value:list[Identifier]):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_tags', value)
        
# CUSTOM
# OnNeighborUpdate - Only updates when a new block has been placed nearby


class BlockState:
    def __init__(self, id:Identifier|str=None, *values:str):
        """
        Base state class for blocks
        """
        self.id = Identifier(id)
        self.values = list(values)

    def __str__(self) -> str:
        return str(self.id)

    @property
    def __dict__(self) -> list:
        data = {
            str(self.id): [x for x in self.values]
        }
        return data
           
    @property
    def id(self) -> Identifier:
        return getattr(self, '_id')
    
    @id.setter
    def id(self, value:Identifier):
        setattr(self, '_id', Identifier(value))
 
    @property
    def values(self) -> list:
        return getattr(self, '_values', [])
    
    @values.setter
    def values(self, value:list):
        def _default(o):
            if isinstance(o, bool):
                return o
            elif isinstance(o, (int, float)):
                return o
            else:
                return str(o)
        if value is None: self.values = []
        elif isinstance(value, list):
            v = [_default(x) for x in value]
            setattr(self, '_values', v)
        else:
            raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
    
    @classmethod
    def from_dict(cls, data:list) -> Self:
        self = cls.__new__(cls)
        return self

# STATES
        
STATES:dict[list] = {}
def state(cls):
    """
    Add this state to the parser
    """
    def wrapper():
        if not issubclass(cls, BlockState): raise TypeError(f"Expected BlockState but got '{cls.__name__}' instead")
        global STATES
        STATES[cls.id] = cls
        return cls
    return wrapper()

# BASES

class BooleanState(BlockState):
    def __init__(self, id:Identifier):
        """
        True or False blockstate. default: True
        """
        BlockState.__init__(self, id, False, True)
   
class IntegerState(BlockState):
    def __init__(self, id:Identifier, stop:int, start:int=0):
        BlockState.__init__(self, id, *range(start, stop+1))
        
# VANILLA

@state
class BlockFaceState(BlockState):
    id = Identifier('block_face')
    def __init__(self):
        BlockState.__init__(self, "down", "up", "north", "south", "east", "west")

@state
class VerticalHalfState(BlockState):
    id = Identifier('vertical_half')
    def __init__(self):
        BlockState.__init__(self, "bottom", "up")

@state
class CardinalDirectionState(BlockState):
    id = Identifier('cardinal_direction')
    def __init__(self):
        BlockState.__init__(self, "north", "south", "east", "west")

@state
class FacingDirectionState(BlockState):
    id = Identifier('facing_direction')
    def __init__(self):
        BlockState.__init__(self, "down", "up", "north", "south", "east", "west")

@state
class ActiveState(BooleanState):
    id = Identifier('active')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class AgeState(BlockState):
    id = Identifier('age')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
        
@state
class AgeBitState(BooleanState):
    id = Identifier('age_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class AllowUnderwaterBitState(BooleanState):
    id = Identifier('allow_underwater_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class AttachedBitState(BooleanState):
    id = Identifier('attached_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class AttachmentState(BlockState):
    id = Identifier('attachment')
    def __init__(self):
        BlockState.__init__(self, 'standing', 'hanging', 'side', 'multiple')
        
@state
class BambooLeafSizeState(BlockState):
    id = Identifier('bamboo_leaf_size')
    def __init__(self):
        BlockState.__init__(self, 'no_leaves', 'small_leaves', 'large_leaves')
        
@state
class BambooStalkThicknessState(BlockState):
    id = Identifier('bamboo_stalk')
    def __init__(self):
        BlockState.__init__(self, 'thin', 'thick')
        
@state
class BigDripleafTiltState(BlockState):
    id = Identifier('bigt_dripleaf_tilt')
    def __init__(self):
        BlockState.__init__(self, 'none', 'unstable', 'partial_tilt','full_tilt')
        
@state
class BiteCounterState(BlockState):
    id = Identifier('bite_counter')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6)
        
@state
class BooksStoredState(BlockState):
    id = Identifier('books_stored')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6)
        
@state
class BrewingStandSlotABitState(BooleanState):
    id = Identifier('brewing_stand_slot_a_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class BrewingStandSlotBBitState(BooleanState):
    id = Identifier('brewing_stand_slot_b_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class BrewingStandSlotCBitState(BooleanState):
    id = Identifier('brewing_stand_slot_c_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class BrushedProgressState(BlockState):
    id = Identifier('brushed_progress')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3)
        
@state
class ButtonPressedBitState(BooleanState):
    id = Identifier('button_pressed_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class CandlesState(BlockState):
    id = Identifier('candles')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3)
        
@state
class CauldronLiquidState(BlockState):
    id = Identifier('cauldron_liquid')
    def __init__(self):
        BlockState.__init__(self, 'water', 'lava')
        
@state
class ChemistryTableTypeState(BlockState):
    id = Identifier('chemistry_table_type')
    def __init__(self):
        BlockState.__init__(self, 'compound_creator', 'material_reducer', 'element_constructor', 'lab_table')
        
@state
class ChiselTypeState(BlockState):
    id = Identifier('chisel_type')
    def __init__(self):
        BlockState.__init__(self, 'default', 'chiseled', 'lines', 'smooth')
        
@state
class ClusterCountState(BlockState):
    id = Identifier('cluster_count')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3)
        
@state
class ColorState(BlockState):
    id = Identifier('color')
    def __init__(self):
        BlockState.__init__(self, 'white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'silver', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black')
        
@state
class ColorBitState(BooleanState):
    id = Identifier('color_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class ConditionalBitState(BooleanState):
    id = Identifier('conditional_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class CoralColorState(BlockState):
    id = Identifier('coral_color')
    def __init__(self):
        BlockState.__init__(self, 'blue', 'pink', 'purple', 'red', 'yellow', 'blue', 'blue dead', 'pink dead', 'red dead', 'yelliow dead')
        
@state
class CoralDirectionState(BlockState):
    id = Identifier('coral_direction')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3)
        
@state
class CoralHangTypeBitState(BooleanState):
    id = Identifier('coral_hang_type_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class CoveredBitState(BooleanState):
    id = Identifier('coverted_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class CrackedState(BlockState):
    id = Identifier('cracked_state')
    def __init__(self):
        BlockState.__init__(self, 'no_cracks', 'cracked', 'max_cracked')
        
@state
class CraftingState(BooleanState):
    id = Identifier('crafting')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class DamageState(BlockState):
    id = Identifier('damage')
    def __init__(self):
        BlockState.__init__(self, 'undamaged', 'slightly_damaged', 'very_damaged', 'broken')
        
@state
class DeadBitState(BooleanState):
    id = Identifier('dead_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class DirectionState(BlockState):
    id = Identifier('direction')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3)
        
@state
class DirtTypeState(BlockState):
    id = Identifier('dirt_type')
    def __init__(self):
        BlockState.__init__(self, 'normal', 'coarse')
        
@state
class DisarmedBitState(BooleanState):
    id = Identifier('disarmed_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class DoorHingeBitState(BooleanState):
    id = Identifier('door_hinge_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class DoublePlantTypeState(BlockState):
    id = Identifier('double_plant_type')
    def __init__(self):
        BlockState.__init__(self, 'sunflower', 'syringa', 'grass', 'fern', 'rose', 'paeonia')
        
@state
class DragDownState(BooleanState):
    id = Identifier('drag_down')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class DripstoneThicknessState(BlockState):
    id = Identifier('dripstone_thickness')
    def __init__(self):
        BlockState.__init__(self, 'tip', 'frustum', 'base', 'middle', 'merge')
        
@state
class EndPortalEyeBitState(BooleanState):
    id = Identifier('end_portal_eye_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class ExplodeBitState(BooleanState):
    id = Identifier('explode_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class FacingDirectionState(BlockState):
    id = Identifier('facing_direction')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5)
        
@state
class FillLevelState(BlockState):
    id = Identifier('fill_level')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6)
        
@state
class FlowerTypeState(BlockState):
    id = Identifier('flower_type')
    def __init__(self):
        BlockState.__init__(self, 'poppy', 'orchid', 'allium', 'houstonia', 'tulip_red', 'tulip_orange', 'tulip_white', 'tulip_pink', 'oxeye', 'cornflower', 'lily_of_the_valley')
        
@state
class GroundSignDirectionState(BlockState):
    id = Identifier('ground_sign_direction')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
        
@state
class GrowthState(BlockState):
    id = Identifier('growth')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6,7)
        
@state
class HangingState(BooleanState):
    id = Identifier('hanging')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class HeadPieceBitState(BooleanState):
    id = Identifier('head_piece_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class HeightState(BlockState):
    id = Identifier('height')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6,7)
        
@state
class HugeMushroomBitsState(BlockState):
    id = Identifier('huge_mushroom_bit')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
        
@state
class InWallBitState(BooleanState):
    id = Identifier('in_wall_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class InfiniburnBitState(BooleanState):
    id = Identifier('infiniburn_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class ItemFrameMapBitState(BooleanState):
    id = Identifier('item_frame_map_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class ItemFramePhotoBitState(BooleanState):
    id = Identifier('item_frame_photo_bit')
    def __init__(self):
        BooleanState.__init__(self)
 
@state
class LiquidDepthState(BlockState):
    id = Identifier('liquid_depth')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
        
@state
class MoisturizedAmountState(BlockState):
    id = Identifier('moisturized_amount')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6,7)
        
@state
class MonsterEggStoneTypeState(BlockState):
    id = Identifier('monster_egg_stone_type')
    def __init__(self):
        BlockState.__init__(self, 'stone', 'cobblestone', 'stone_brick', 'mossy_stone_brick', 'cracked_stone_brick', 'chiseled_stone_brick')
        
@state
class NewLeafTypeState(BlockState):
    id = Identifier('new_leaf_type')
    def __init__(self):
        BlockState.__init__(self, 'acacia', 'dark_oak')
        
@state
class NewLogTypeState(BlockState):
    id = Identifier('new_log_type')
    def __init__(self):
        BlockState.__init__(self, 'acacia', 'dark_oak')
        
@state
class NoDropBitState(BooleanState):
    id = Identifier('no_drop_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class OccupiedBitState(BooleanState):
    id = Identifier('occupied_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class OldLeafTypeState(BlockState):
    id = Identifier('old_leaf_type')
    def __init__(self):
        BlockState.__init__(self, 'oak', 'spruce', 'birch', 'jungle')
        
@state
class OldLogTypeState(BlockState):
    id = Identifier('old_log_type')
    def __init__(self):
        BlockState.__init__(self, 'oak', 'spruce', 'birch', 'jungle')
        
@state
class OpenBitState(BooleanState):
    id = Identifier('open_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class OrientationState(BooleanState):
    id = Identifier('orientation')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class OutputLitBitState(BooleanState):
    id = Identifier('output_lit_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class OutputSubtractBitState(BooleanState):
    id = Identifier('output_subtract_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class PersistentBitState(BooleanState):
    id = Identifier('persistent_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class PortalAxisState(BlockState):
    id = Identifier('portal_axis')
    def __init__(self):
        BlockState.__init__(self, 'unknown', 'x', 'z')
        
@state
class PoweredBitState(BooleanState):
    id = Identifier('powered_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class RailDataBitState(BooleanState):
    id = Identifier('rail_data_bit')
    def __init__(self):
        BooleanState.__init__(self)
        
@state
class RailDirectionState(BlockState):
    id = Identifier('rail_direction')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6,7,8)
        
@state
class RedstoneSignalState(BlockState):
    id = Identifier('redstone_signal')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6,7,8,9, 10,11,12,13,14,15)
        
@state
class RepeaterDelayState(BlockState):
    id = Identifier('repeater_delay')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3)
        
@state
class SandStoneTypeState(BlockState):
    id = Identifier('sand_stone_type')
    def __init__(self):
        BlockState.__init__(self, 'default', 'heiroglyphs', 'cut', 'smooth')
        
@state
class SandTypeState(BlockState):
    id = Identifier('sand_type')
    def __init__(self):
        BlockState.__init__(self, 'normal', 'type')

@state
class SaplingTypeState(BlockState):
    id = Identifier('sapling_type')
    def __init__(self):
        BlockState.__init__(self, 'evergreen', 'birch', 'jungle', 'acacia', 'roofed_oak')

@state
class SculkSensorPhaseState(BlockState):
    id = Identifier('sculk_sensor_phase')
    def __init__(self):
        BlockState.__init__(self, 'inactive', 'active', 'cooldown')

@state
class SeaGrassTypeState(BlockState):
    id = Identifier('sea_grass_type')
    def __init__(self):
        BlockState.__init__(self, 'default', 'double_top', 'double_bot')

@state
class SpongeTypeState(BlockState):
    id = Identifier('sponge_type')
    def __init__(self):
        BlockState.__init__(self, 'dry', 'wet')

@state
class StabilityState(BlockState):
    id = Identifier('stability')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5)

@state
class StabilityCheckState(BooleanState):
    id = Identifier('stability_check')
    def __init__(self):
        BooleanState.__init__(self)

@state
class StoneBrickTypeState(BlockState):
    id = Identifier('stone_brick_type')
    def __init__(self):
        BlockState.__init__(self, 'default', 'mossy', 'cracked', 'chiseled', 'smooth')

@state
class StoneSlabTypeState(BlockState):
    id = Identifier('stone_slab_type')
    def __init__(self):
        BlockState.__init__(self, 'smooth_stone', 'sandstone', 'wood', 'cobblestone', 'brick', 'stone_brick', 'quartz', 'nether_brick')

@state
class StoneSlabType2State(BlockState):
    id = Identifier('stone_slab_type2')
    def __init__(self):
        BlockState.__init__(self, 'red_sandstone', 'purpur', 'prismarine_rough', 'prismarine_dark', 'prismarine_brick', 'mossy_cobblestone', 'smooth_sandstone', 'red_nether_brick')

@state
class StoneSlabType3State(BlockState):
    id = Identifier('stone_slab_type3')
    def __init__(self):
        BlockState.__init__(self, 'end_stone_brick', 'smooth_red_sandstone', 'polishe_andesite', 'andesite', 'diorite', 'polished_diorite', 'granite', 'polished_granite')

@state
class StoneSlabType4State(BlockState):
    id = Identifier('stone_slab_type_4')
    def __init__(self):
        BlockState.__init__(self, 'mossy_stone_brick', 'smooth_quartz', 'stone', 'cut_sandstone', 'cut_red_sandstone')

@state
class StoneTypeState(BlockState):
    id = Identifier('stone_type')
    def __init__(self):
        BlockState.__init__(self, 'stone', 'granite', 'granite_smooth', 'diorite', 'diorite_smooth', 'andesite', 'andesite_smooth')

@state
class StrippedBitState(BooleanState):
    id = Identifier('stripped_bit')
    def __init__(self):
        BooleanState.__init__(self)

@state
class StructureBlockTypeState(BlockState):
    id = Identifier('structure_block_type')
    def __init__(self):
        BlockState.__init__(self,'data', 'save', 'load', 'corner', 'invalid', 'export' )

@state
class StructureVoidTypeState(BlockState):
    id = Identifier('structure_void_type')
    def __init__(self):
        BlockState.__init__(self, 'void', 'air')

@state
class SuspendedBitState(BooleanState):
    id = Identifier('suspended_bit')
    def __init__(self):
        BooleanState.__init__(self)

@state
class TallGrassTypeState(BlockState):
    id = Identifier('tall_grass_type')
    def __init__(self):
        BlockState.__init__(self, 'default', 'tall', 'fern', 'snow')

@state
class ToggleBitState(BooleanState):
    id = Identifier('toggle_bit')
    def __init__(self):
        BooleanState.__init__(self)

@state
class TopSlotBitState(BooleanState):
    id = Identifier('top_slot_bit')
    def __init__(self):
        BooleanState.__init__(self)

@state
class TorchFacingDirectionState(BlockState):
    id = Identifier('torch_facing_direction')
    def __init__(self):
        BlockState.__init__(self, 'unknown', 'west', 'east', 'north', 'south', 'top')

@state
class TriggedBitState(BooleanState):
    id = Identifier('triggered_bit')
    def __init__(self):
        BooleanState.__init__(self)

@state
class TurtleEggCountState(BlockState):
    id = Identifier('turtle_egg_count')
    def __init__(self):
        BlockState.__init__(self, 'one_egg', 'two_egg', 'three_egg', 'four_egg')

@state
class UpdateBitState(BooleanState):
    id = Identifier('update_bit')
    def __init__(self):
        BooleanState.__init__(self)

@state
class UpperBlockBitState(BooleanState):
    id = Identifier('upper_block_bit')
    def __init__(self):
        BooleanState.__init__(self)

@state
class UpsideDownBitState(BooleanState):
    id = Identifier('upside_down_bit')
    def __init__(self):
        BooleanState.__init__(self)

@state
class VineDirectionBitsState(BlockState):
    id = Identifier('vine_direction_bits')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)

@state
class WallBlockTypeState(BlockState):
    id = Identifier('wall_block_type')
    def __init__(self):
        BlockState.__init__(self, 'cobblestone', 'mossy_cobblestone', 'granite', 'diorite', 'andesite', 'sandstone', 'brick', 'stone_brick', 'mossy_stone_brick', 'nether_brick', 'end_brick', 'prismarine', 'red_sandstone', 'red_nether_brick')

@state
class WallConnectionTypEastState(BlockState):
    id = Identifier('wall_connection_type_east')
    def __init__(self):
        BlockState.__init__(self, 'none', 'short', 'tall')

@state
class WallConnectionTypeNorthState(BlockState):
    id = Identifier('wall_connection_type_north')
    def __init__(self):
        BlockState.__init__(self, 'none', 'short', 'tall')

@state
class WallConnectionTypeSouthState(BlockState):
    id = Identifier('wall_connection_type_south')
    def __init__(self):
        BlockState.__init__(self, 'none', 'short', 'tall')

@state
class WallConnectionTypeWestState(BlockState):
    id = Identifier('wall_connection_type_west')
    def __init__(self):
        BlockState.__init__(self, 'none', 'short', 'tall')

@state
class WallPostBitState(BooleanState):
    id = Identifier('wall_post_bit')
    def __init__(self):
        BooleanState.__init__(self)

@state
class WeirdoDirectionState(BlockState):
    id = Identifier('weirdo_direction')
    def __init__(self):
        BlockState.__init__(self, 0,1,2,3)

@state
class WoodTypeState(BlockState):
    id = Identifier('wood_type')
    def __init__(self):
        BlockState.__init__(self, 'oak', 'spruce', 'birch', 'jungle', 'acacia', 'dark_oak')

# TRAITS
       
class BlockTrait:
    def __init__(self, enabled_states:list[BlockState]):
        """
        Base trait class for blocks
        """
        self.enabled_states = enabled_states

    @property
    def __dict__(self) -> dict:
        data = {
            'enabled_states': [str(x.id) for x in self.enabled_states]
        }
        return data

    @property
    def id(self) -> Identifier:
        return getattr(self, '_id')
    
    @id.setter
    def id(self, value:Identifier):
        setattr(self, '_id', Identifier(value))

    @property
    def enabled_states(self) -> list[BlockState]:
        return getattr(self, '_enabled_states', [])
    
    @enabled_states.setter
    def enabled_states(self, value:list[BlockState]):
        if value is None: self.enabled_states = []
        elif isinstance(value, list):
            v = []
            for x in value:
                if not issubclass(x, BlockState):
                    raise TypeError(f"Expected BlockState but got '{x.__class__.__name__}' instead")
                v.append(x)
            setattr(self, '_enabled_states', v)
        else:
            raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
    
    @classmethod
    def from_dict(cls, data:dict) -> Self:
        self = cls.__new__(cls)
        if 'enabled_states' in data: self.enabled_states = data.pop('enabled_states')
        return self

TRAITS:dict[str, BlockTrait] = {}
def trait(cls):
    """
    Add this trait to the parser
    """
    def wrapper():
        if not issubclass(cls, BlockTrait): raise TypeError(f"Expected BlockTrait but got '{cls.__name__}' instead")
        global TRAITS
        TRAITS[cls.id] = cls
        return cls
    return wrapper()

@trait
class PlacementDirectionTrait(BlockTrait):
    id = Identifier('placement_direction')
    def __init__(self, enabled_states:list[BlockState]=[], y_rotation_offset:float=0.0):
        """
        Adds the CardinalDirectionState and/or FacingDirectionState states and setter function to the block. The values of these states are set when the block is placed.

        :param enabled_states: Which states to enable. Must specify at least one, defaults to []
        :type enabled_states: list[BlockState], optional
        :param y_rotation_offset: The y rotation offset to apply to the block. Must be [0.0, 90.0, 180.0, 270.0]. Default is 0, meaning if the player is facing north, the CardinalDirectionState and/or FacingDirectionState state will be north, defaults to 0.0
        :type y_rotation_offset: float, optional
        """
        for state in enabled_states:
            if not issubclass(state, (CardinalDirectionState, FacingDirectionState)): raise TypeError(f"Expected CardinalDirectionState or FacingDirectionState but got '{state.__class__.__name__}' instead")
        BlockTrait.__init__(self, enabled_states)
        if y_rotation_offset not in [0.0, 90.0, 180.0, 270.0, 0, 90, 180, 270]: raise ValueError(y_rotation_offset)
        self.y_rotation_offset = y_rotation_offset

    @property
    def __dict__(self) -> dict:
        data = super().__dict__
        if self.y_rotation_offset != 0: data['y_rotation_offset'] = self.y_rotation_offset
        return data

    @property
    def y_rotation_offset(self) -> float:
        return getattr(self, '_y_rotation_offset', 0.0)
    
    @y_rotation_offset.setter
    def y_rotation_offset(self, value:float):
        if value is None: self.y_rotation_offset = 0.0
        elif isinstance(value, float):
            setattr(self, '_y_rotation_offset', value)
        else:
            raise TypeError(f"Expected float but got '{value.__class__.__name__}' instead")

    @classmethod
    def from_dict(cls, data:dict) -> Self:
        self = super().from_dict(data)
        if 'y_rotation_offset' in data: self.y_rotation_offset = data.pop('y_rotation_offset')
        return self

    @classmethod
    def cardinal(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([CardinalDirectionState])`
        """
        self = cls.__new__(cls)
        enabled_states = [CardinalDirectionState]
        BlockTrait.__init__(self, enabled_states)
        self.y_rotation_offset = 0.0
        return self
    
    @classmethod
    def facing(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([FacingDirectionState])`
        """
        self = cls.__new__(cls)
        enabled_states = [FacingDirectionState]
        BlockTrait.__init__(self, enabled_states)
        self.y_rotation_offset = 0.0
        return self
    
    @classmethod
    def all(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([CardinalDirectionState, FacingDirectionState])`
        """
        self = cls.__new__(cls)
        enabled_states = [CardinalDirectionState, FacingDirectionState]
        BlockTrait.__init__(self, enabled_states)
        self.y_rotation_offset = 0.0
        return self

@trait
class PlacementPositionTrait(BlockTrait):
    id = Identifier('placement_position')
    def __init__(self, enabled_states:list[BlockState]=[]):
        """
        Adds the BlockFaceState and/or VerticalHalfState BlockStates. The value of these state(s) are set when the block is placed.

        :param enabled_states: Which states to enable. Must specify at least one, defaults to []
        :type enabled_states: list[BlockState], optional
        """
        for state in enabled_states:
            if not issubclass(state, (BlockFaceState, VerticalHalfState)): raise TypeError(f"Expected BlockFaceState or VerticalHalfState but got '{state.__class__.__name__}' instead")
        BlockTrait.__init__(self, enabled_states)

    @classmethod
    def block_face(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([BlockFaceState])`
        """
        self = cls.__new__(cls)
        enabled_states = [BlockFaceState]
        BlockTrait.__init__(self, enabled_states)
        return self
    
    @classmethod
    def vertical_half(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([VerticalHalfState])`
        """
        self = cls.__new__(cls)
        enabled_states = [VerticalHalfState]
        BlockTrait.__init__(self, enabled_states)
        return self
    
    @classmethod
    def all(cls) -> Self:
        """
        Equivalent to: `PlacementPositionTrait([BlockFaceState, VerticalHalfState])`
        """
        self = cls.__new__(cls)
        enabled_states = [BlockFaceState, VerticalHalfState]
        BlockTrait.__init__(self, enabled_states)
        return self
    
# BLOCK

class BlockPermutation:
    def __init__(self, condition:Molang|str):
        self.condition = Molang.parse(condition)
        self.components:dict[Identifier, BlockComponent] = {}

    @property
    def __dict__(self) -> dict:
        data = {
            'condition': str(self.condition),
            'components': {}
        }
        for k,v in self.components.items():
            data['components'][str(k)] = v.__dict__
        return data

    @property
    def condition(self) -> Molang:
        return getattr(self, '_condition')
    
    @condition.setter
    def condition(self, value:Molang):
        if not isinstance(value, Molang): raise TypeError(f"Expected Molang but got '{value.__class__.__name__}' instead")
        setattr(self, '_condition', value)

    @property
    def components(self) -> dict[Identifier, BlockComponent]:
        return getattr(self, '_components')
    
    @components.setter
    def components(self, value:dict[Identifier, BlockComponent]):
        if not isinstance(value, dict): raise TypeError(f"Expected dict but got '{value.__class__.__name__}' instead")
        setattr(self, '_components', value)

    def add_component(self, component:BlockComponent) -> BlockComponent:
        if not isinstance(component, BlockComponent): raise TypeError(f"Expected BlockComponent but got '{component.__class__.__name__}' instead")
        self.components[component.id] = component
        return component

    def get_component(self, id:Identifier|str) -> BlockComponent:
        i = Identifier.parse(id)
        return self.components[i]

    def remove_component(self, id:Identifier|str) -> BlockComponent:
        i = Identifier.parse(id)
        e = self.components[i]
        del self.components[i]
        return e

    def clear_components(self) -> Self:
        self.components = {}
        return self

# TODO: Add redstone method to create custom redstone components.
class Block(Saveable):
    format_version = '1.20.51'
    id = Identifier('block')
    def __init__(self, identifier:Identifier|str, menu_category:MenuCategory=None):
        self.identifier = Identifier.parse(identifier)
        self.menu_category = menu_category
        self.components:dict[str, BlockComponent] = {}
        self.permutation:list[BlockPermutation] = []
        self.events:dict[Identifier, Event] = {}
        self.traits:dict[Identifier, BlockTrait] = {}
        self.states:dict[Identifier, list[str]] = {}

    @property
    def __dict__(self) -> dict:
        block = {
            'description': {
                'identifier': str(self.identifier)
            }
        }
        if self.menu_category:
            block['description']['menu_category'] = self.menu_category.__dict__

        if self.traits:
            block['description']['traits'] = {}
            for k,v in self.traits.items():
                block['description']['traits'][str(k)] = v.__dict__

        if self.states:
            block['description']['states'] = {}
            for k,v in self.states.items():
                block['description']['states'].update(v.__dict__)
            
        if self.components:
            block['components'] = {}
            for k,v in self.components.items():
                block['components'][str(k)] = v.__dict__
                        
        if self.permutation:
            block['permutation'] = []
            for v in self.permutation:
                block['permutation'].append(v.__dict__)
    
        if self.events:
            block['events'] = {}
            for key, events in self.events.items():
                d = {}
                for k,v in events.items():
                    d[k.path] = v.__dict__
                block['events'][str(key)] = d

        data = {
            'format_version': self.format_version,
            str(self.id): block
        }
        if self.type:
            data['type'] = str(self.type)
        return data
     
    @property
    def type(self) -> Identifier:
        return getattr(self, '_type', None)
    
    @type.setter
    def type(self, value:Identifier):
        setattr(self, '_type', Identifier(value))

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
    def identifier(self) -> Identifier:
        return getattr(self, '_identifier')
    
    @identifier.setter
    def identifier(self, value:Identifier):
        if not isinstance(value, Identifier): raise TypeError(f"Expected Identifier but got '{value.__class__.__name__}' instead")
        setattr(self, '_identifier', Identifier(value))

    @property
    def components(self) -> dict[str, BlockComponent]:
        return getattr(self, '_components')
    
    @components.setter
    def components(self, value:dict[str, BlockComponent]):
        if not isinstance(value, dict): raise TypeError(f"Expected dict but got '{value.__class__.__name__}' instead")
        setattr(self, '_components', value)

    @property
    def permutation(self) -> list[BlockPermutation]:
        return getattr(self, '_permutation')
    
    @permutation.setter
    def permutation(self, value:list[BlockPermutation]):
        if not isinstance(value, list): raise TypeError(f"Expected list but got '{value.__class__.__name__}' instead")
        setattr(self, '_permutation', value)

    @property
    def events(self) -> dict[Identifier, Event]:
        return getattr(self, '_events')
    
    @events.setter
    def events(self, value:dict[Identifier, Event]):
        if not isinstance(value, dict): raise TypeError(f"Expected dict but got '{value.__class__.__name__}' instead")
        setattr(self, '_events', value)

    @property
    def states(self) -> dict[Identifier, BlockState]:
        return getattr(self, '_states')

    @states.setter
    def states(self, value:dict[Identifier, BlockState]):
        if not isinstance(value, dict): raise TypeError(f"Expected dict but got '{value.__class__.__name__}' instead")
        setattr(self, '_states', value)
    
    @classmethod
    def from_dict(cls, data:dict) -> Self:
        self = cls.__new__(cls)
        if str(self.id) in data:
            block = data['minecraft:block']
            if 'description' in block:
                desc = block['description']
                if 'identifier' in desc:
                    self.identifier = desc['identifier']
                    
            if 'components' in block:
                comp = block['components']
                    
            if 'permutation' in block:
                perm = block['permutation']
                    
            if 'events' in block:
                events = block['events']
        return self

    # COMPONENT

    def add_component(self, component:BlockComponent) -> BlockComponent:
        if not isinstance(component, BlockComponent): raise TypeError(f"Expected BlockComponent but got '{component.__class__.__name__}' instead")
        if isinstance(component, Trigger): component.event.namespace = self.identifier.namespace
        self.components[component.id] = component
        return component

    def get_component(self, id:str) -> BlockComponent:
        x = id.id if isinstance(id, BlockComponent) else Identifier(id)
        return self.components.get(x)

    def remove_component(self, id:str) -> BlockComponent:
        x = id.id if isinstance(id, BlockComponent) else Identifier(id)
        return self.components.pop(x)

    def clear_components(self) -> Self:
        self.components.clear()
        return self
    
    # EVENT
    def _event_id(self, id:Identifier|str):
        if id is None:
            return 'default'
        elif isinstance(id, Identifier):
            return id
        else:
            return self.identifier.copy_with_path(id)

    def add_event(self, id:Identifier|str, event:Event) -> Event:
        if isinstance(event, Event):
            k  = self._event_id(id)
            if k in self.events:
                self.events[k][event.id] = event
                return event 
            self.events[k] = {}
            return self.add_event(id, event)
        elif isinstance(event, list):
            x = Sequence()
            for e in event: x.add_event(e)
            return self.add_event(id, x)
        else:
            raise TypeError(f"Expected BlockEvent but got '{event.__class__.__name__}' instead")

    def get_event(self, id:Identifier|str) -> Event:
        k = self._event_id(id)
        return self.events.get(k)

    def remove_event(self, id:Identifier|str) -> Event:
        i = Identifier.parse(id)
        return self.events.pop(i)

    def clear_events(self) -> Self:
        self.events.clear()
        return self
    
    # PERMUTATION

    def add_permutation(self, permutation:BlockPermutation) -> BlockPermutation:
        if not isinstance(permutation, BlockPermutation): raise TypeError(f"Expected BlockPermutation but got '{permutation.__class__.__name__}' instead")
        self.permutation.append(permutation)
        return permutation

    def get_permutation(self, index:int) -> BlockPermutation:
        return self.permutation[index]

    def remove_permutation(self, index:int) -> BlockPermutation:
        p = self.get_permutation(index)
        del self.permutation[index]
        return p

    def clear_permutation(self) -> Self:
        self.permutation.clear()
        return self

    # TRAIT

    def add_trait(self, trait:BlockTrait) -> BlockTrait:
        if not isinstance(trait, BlockTrait): raise TypeError(f"Expected BlockTrait but got '{trait.__class__.__name__}' instead")
        self.traits[trait.id] = trait
        return trait

    def get_trait(self, id:str) -> BlockTrait:
        x = id.id if isinstance(id, BlockTrait) else Identifier(id)
        return self.traits.get(x)

    def remove_trait(self, id:str) -> BlockTrait:
        x = id.id if isinstance(id, BlockTrait) else Identifier(id)
        return self.traits.pop(x)

    def clear_trait(self) -> Self:
        self.traits.clear()
        return self

    # STATE

    def add_state(self, state:BlockState) -> BlockState:
        if not isinstance(state, BlockState): raise TypeError(f"Expected BlockState but got '{state.__class__.__name__}' instead")
        self.states[state.id] = state
        return state

    def get_state(self, id:Identifier|str) -> BlockState:
        x = id.id if isinstance(id, BlockState) else Identifier(id)
        return self.states.get(x)

    def remove_state(self, id:Identifier|str) -> BlockState:
        x = id.id if isinstance(id, BlockState) else Identifier(id)
        return self.states.pop(x)

    def clear_state(self) -> Self:
        self.states.clear()
        return self

# ASSETS+ https://www.curseforge.com/minecraft-bedrock/addons/assets-plus
# The following classes require Assets+. See homepage for more info

# TODO
# - Add optional "material" to all block classes, defaults 'minecraft:stone'. Make "MaterialInstancesComponent" a class parameter

class SlabBlock(Block):
    type = Identifier('slab')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id, MenuCategory(Category.CONSTRUCTION, 'itemGroup.name.slab'))
        if material is None: material = Material(id.replace('slab', ''))
        self.add_trait(PlacementPositionTrait.vertical_half())
        
        # STATES

        self.shape = self.add_state(BlockState(self.identifier.copy_with_path('shape'), 'single', 'double'))

        # COMPONENTS

        self.add_component(OnInteractComponent('on_interact', Molang(f"q.block_state('{self.shape}')=='single'")))

        # PERMUTATIONS

        perm1 = BlockPermutation(Molang(f"q.block_state('{self.shape}')=='single'"))
        perm1.add_component(GeometryComponent('geometry.template_slab'))
        self.add_permutation(perm1)

        perm2 = BlockPermutation(Molang(f"q.block_state('{self.shape}')=='double'"))
        perm2.add_component(GeometryComponent('geometry.cube'))
        self.add_permutation(perm2)

        perm3 = BlockPermutation(Molang("q.block_state('minecraft:vertical_half')=='top'"))
        perm1.add_component(TransformationComponent(rotation=[0,0,0]))
        self.add_permutation(perm3)

        perm4 = BlockPermutation(Molang("q.block_state('minecraft:vertical_half')=='bottom'"))
        perm1.add_component(TransformationComponent(rotation=[0,0,0]))
        self.add_permutation(perm4)

        # EVENTS

        self.add_event('on_interact', RunCommand(['playsound use.stone @p'], EventTarget.PLAYER))
        self.add_event('on_interact', SetBlockState({self.shape.id: "'double'"}))

class StairsBlock(Block):
    type = Identifier('stairs')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id, MenuCategory(Category.CONSTRUCTION, 'itemGroup.name.stairs'))
        if material is None: material = Material(id.replace('stairs', ''))
        self.add_trait(PlacementDirectionTrait.cardinal())
        self.add_trait(PlacementPositionTrait.vertical_half())

        # STATES
        
        self.shape = self.add_state(BlockState(self.identifier.copy_with_path('shape'), 'straight', 'inner_left', 'inner_right', 'outer_left', 'outer_right'))

        # PERMUTATIONS
        perm1 = BlockPermutation(Molang("q.block_state('minecraft:vertical_half')=='north'&&q.block_state('minecraft:vertical_half')=='bottom'"))
        perm1.add_component(TransformationComponent(rotation=[0,0,0]))
        self.add_permutation(perm1)

        perm2 = BlockPermutation(Molang("q.block_state('minecraft:vertical_half')=='south'&&q.block_state('minecraft:vertical_half')=='bottom'"))
        perm2.add_component(TransformationComponent(rotation=[0,180,0]))
        self.add_permutation(perm2)

        perm3 = BlockPermutation(Molang("q.block_state('minecraft:vertical_half')=='east'&&q.block_state('minecraft:vertical_half')=='bottom'"))
        perm3.add_component(TransformationComponent(rotation=[0,90,0]))
        self.add_permutation(perm3)

        perm4 = BlockPermutation(Molang("q.block_state('minecraft:vertical_half')=='west'&&q.block_state('minecraft:vertical_half')=='bottom'"))
        perm4.add_component(TransformationComponent(rotation=[0,-90,0]))
        self.add_permutation(perm4)
        
        perm5 = BlockPermutation(Molang("q.block_state('minecraft:vertical_half')=='north'&&q.block_state('minecraft:vertical_half')=='top'"))
        perm5.add_component(TransformationComponent(rotation=[180,0,0]))
        self.add_permutation(perm5)

        perm6 = BlockPermutation(Molang("q.block_state('minecraft:vertical_half')=='south'&&q.block_state('minecraft:vertical_half')=='top'"))
        perm6.add_component(TransformationComponent(rotation=[180,180,0]))
        self.add_permutation(perm6)

        perm7 = BlockPermutation(Molang("q.block_state('minecraft:vertical_half')=='east'&&q.block_state('minecraft:vertical_half')=='top'"))
        perm7.add_component(TransformationComponent(rotation=[180,90,0]))
        self.add_permutation(perm7)

        perm8 = BlockPermutation(Molang("q.block_state('minecraft:vertical_half')=='west'&&q.block_state('minecraft:vertical_half')=='top'"))
        perm8.add_component(TransformationComponent(rotation=[180,-90,0]))
        self.add_permutation(perm8)

        # EVENTS

class CropBlock(Block):
    type = Identifier('crop')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id, RenderMethod.ALPHA_TEST)
        
        # STATES

        self.age = self.add_state(IntegerState(self.identifier.copy_with_path('age'), 7))
        
        # COMPONENTS

        self.add_component(LootComponent('loot_tables/morefood/blocks/coffee.json'))
        self.add_component(LightDampeningComponent(0))
        self.add_component(LightEmissionComponent(0))
        self.add_component(DestructibleByExplosionComponent(0))
        self.add_component(DestructibleByMiningComponent(0))
        self.add_component(GeometryComponent('geometry.template_crop'))
        self.add_component(CollisionBoxComponent.none())
        self.add_component(OnInteractComponent(condition=Molang(f"q.is_item_name_any('slot.weapon.mainhand','minecraft:bone_meal') && q.block_state('{ self.age.id }') != 7")))
        self.add_component(RandomTickingComponent(Trigger('increase_age', Molang(f"q.block_state('{ self.age.id }')!=7"))))
        pf = PlacementFilterComponent()
        self.add_component(pf)

        # TODO: PERMUTATIONS
        
        # EVENTS

        self.add_event('bone_meal_growth', DecrementStack())
        self.add_event('bone_meal_growth', Trigger('increase_age'))
        self.add_event('bone_meal_growth', RunCommand(["particle minecraft:crop_growth_emitter ~ ~ ~", "playsound item.bone_meal.use @p ~ ~ ~"]))

        self.add_event('increase_age', IncrementBlockState(self.age.id))

class BushBlock(CropBlock):
    type = Identifier('bush')
    def __init__(self, id:Identifier|str, material:Material=None):
        CropBlock.__init__(self, id)
        if material is None: material = Material(id, RenderMethod.ALPHA_TEST)

        # COMPONENTS
        self.add_component(GeometryComponent('geometry.template_cross'))
        self.add_component(OnInteractComponent())

        # TODO: PERMUTATIONS
        self.clear_permutation() # Clear perms from CropBlock

        # EVENTS
        oi = Sequence()
        oi.set_condition(0, Molang(f"q.is_item_name_any('slot.weapon.mainhand','minecraft:bone_meal') && q.block_state('{ self.age.id }') != 7"))
        oi.add_event(0, Trigger('bone_meal_growth'))
        oi.set_condition(1, Molang(f"q.block_state('{ self.age.id }') >= 4 && q.block_state('{ self.age.id }') <= 6 && !q.is_item_name_any('slot.weapon.mainhand','minecraft:bone_meal')"))
        oi.add_event(1, SpawnLoot('loot_tables/morefood/on_interact/coffee_bush_age2.json'))
        oi.add_event(1, SetBlockState({self.age.id: "'1'"}))
        oi.add_event(1, PlaySound('block.sweet_berry_bush.pick'))
        
        oi.set_condition(2, Molang(f"q.block_state('{ self.age.id }') == 7 && !q.is_item_name_any('slot.weapon.mainhand','minecraft:bone_meal')"))
        oi.add_event(2, SpawnLoot('loot_tables/morefood/on_interact/coffee_bush_age3.json'))
        oi.add_event(2, SetBlockState({self.age.id: "'1'"}))
        oi.add_event(2, PlaySound('block.sweet_berry_bush.pick'))

        self.add_event('on_interact', oi)

class SaplingBlock(Block):
    type = Identifier('sapling')
    def __init__(self, id:Identifier|str, structures:list[Identifier]=[], material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id, RenderMethod.ALPHA_TEST)
        
        # STATES

        self.stage = self.add_state(IntegerState(self.identifier.copy_with_path('stage'), 1))

        # COMPONENTS
        self.add_component(LootComponent(f'loot_tables/blocks/{self.identifier.path}.json'))
        self.add_component(LightDampeningComponent(0))
        self.add_component(LightEmissionComponent(0))
        self.add_component(DestructibleByMiningComponent(0))
        self.add_component(DestructibleByExplosionComponent(0))
        self.add_component(GeometryComponent('geometry.template_cross'))
        self.add_component(CollisionBoxComponent(False))
        self.add_component(OnInteractComponent('bone_meal_growth', "q.is_item_name_any('slot.weapon.mainhand','minecraft:bone_meal')"))
        pf = PlacementFilterComponent()
        self.add_component(pf)
        self.add_component(SelectionBoxComponent([-6.5, 0, -6.5], [13, 12.5, 13]))
        self.add_component(RandomTickingComponent(Trigger('increase_stage')))
        mi = MaterialInstancesComponent()
        mi.add_material('*', material)
        self.add_component(mi)

        # EVENTS
        self.add_event('bone_meal_growth', DecrementStack())
        self.add_event('bone_meal_growth', RunCommand(["particle minecraft:crop_growth_emitter ~ ~ ~", "playsound item.bone_meal.use @p ~ ~ ~"]))
        self.add_event('bone_meal_growth', Trigger('increase_age'))

        increase_age = Sequence()
        increase_age.set_condition(0, Molang(f"q.block_state('{ self.stage }')==1"))
        increase_age.add_event(0, Trigger('generate'))
        increase_age.set_condition(1, Molang(f"q.block_state('{ self.stage }')==0"))
        increase_age.add_event(1, SetBlockState({self.stage.id: "1"}))
        self.add_event('increase_stage', increase_age)

        generate = Sequence()
        generate.add_event(0, RunCommand([ "execute if block ~ ~1 ~ air run setblock ~ ~ ~ air", "execute if block ~ ~1 ~ air run fill ~-2 ~ ~-2 ~2 ~5 ~2 air destroy"]))
        generate.add_event(0, SetBlockAtPos('dirt', [0,-1,0]))
        variants = Randomize()
        for i, j in enumerate(structures):
            variants.add_event(i, RunCommand(f'execute if block ~ ~1 ~ air run structure load {str(Identifier(j))} ~-2 ~ ~-2'))
        generate.add_event(1, variants)
        self.add_event('generate', generate)

class CakeBlock(Block):
    type = Identifier('cake')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id)
        self.candle_cakes = {
            Identifier("candle"): Identifier("candle_cake"),
            Identifier("white_candle"): Identifier("white_candle_cake"),
            Identifier("light_gray_candle"): Identifier("light_gray_candle_cake"),
            Identifier("gray_candle"): Identifier("gray_candle_cake"),
            Identifier("black_candle"): Identifier("black_candle_cake"),
            Identifier("brown_candle"): Identifier("brown_candle_cake"),
            Identifier("red_candle"): Identifier("red_candle_cake"),
            Identifier("orange_candle"): Identifier("orange_candle_cake"),
            Identifier("yellow_candle"): Identifier("yellow_candle_cake"),
            Identifier("lime_candle"): Identifier("lime_candle_cake"),
            Identifier("green_candle"): Identifier("green_candle_cake"),
            Identifier("cyan_candle"): Identifier("cyan_candle_cake"),
            Identifier("light_blue_candle"): Identifier("light_blue_candle_cake"),
            Identifier("blue_candle"): Identifier("blue_candle_cake"),
            Identifier("purple_candle"): Identifier("purple_candle_cake"),
            Identifier("magenta_candle"): Identifier("magenta_candle_cake"),
            Identifier("pink_candle"): Identifier("pink_candle_cake")
        }

        # STATES

        self.bites = self.add_state(IntegerState(self.identifier.copy_with_path('bites'), 6))

        # COMPONENTS
        self.add_component(LootComponent('loot_tables/empty.json'))
        self.add_component(LightDampeningComponent(0))
        self.add_component(LightEmissionComponent(0))
        self.add_component(DestructibleByExplosionComponent(0.5))
        self.add_component(DestructibleByMiningComponent(0.5))
        self.add_component(OnInteractComponent())
        pf = PlacementFilterComponent()
        self.add_component(pf)

        # TODO: PERMUTATIONS

        # EVENTS
        ic = Sequence()
        ic.add_event(0, RunCommand(["playsound random.burp @s ~ ~ ~ 0.50", "effect @s saturation 1 1 true"], EventTarget.PLAYER))
        ic.set_condition(1, Molang(f"q.block_state('{ self.bites.id }')==6"))
        ic.add_event(1, SetBlock('minecraft:air'))
        ic.set_condition(2, Molang(f"q.block_state('{ self.bites.id }')!=6"))
        ic.add_event(2, IncrementBlockState(self.bites.id))
        self.add_event('increase_bites', ic)

        # Convert cake to candle_cake
        c = Sequence()
        for i, v in enumerate(self.candle_cakes.items()):
            c.set_condition(i, Molang(f"q.is_item_name_any('slot.weapon.mainhand','{v[0]}')"))
            c.add_event(i, DecrementStack())
            c.add_event(i, SetBlock(v[1]))
        self.add_event('convert', c)

        oi = Sequence()
        inner = '||'.join([f"q.is_item_name_any('slot.weapon.mainhand','{x}')" for x in self.candle_cakes.keys()])
        oi.set_condition(0, Molang( inner + f"&&q.block_state('{ self.bites.id }')==0"))
        oi.add_event(0, RunCommand('playsound cake.add_candle @p', EventTarget.BLOCK))
        oi.add_event(0, Trigger('convert'))

        inner = ','.join([f"'{x}'" for x in self.candle_cakes.keys()])
        oi.set_condition(1, Molang(f"!q.is_item_name_any('slot.weapon.mainhand',{inner})"))
        oi.add_event(1, Trigger('increase_bites'))
        self.add_event('on_interact', oi)

    def get_candle_cake(self, candle:Identifier) -> Identifier:
        return self.candle_cakes[candle]
    
    def add_candle_cake(self, candle:Identifier, cake:Identifier) -> Identifier:
        self.candle_cakes[candle] = cake
        return candle
    
    def remove_candle_cake(self, candle:Identifier) -> Identifier:
        c = self.candle_cakes[candle]
        del self.candle_cakes[candle]
        return c

    def clear_candle_cakes(self) -> Self:
        self.candle_cakes = {}
        return self    

class CandleCakeBlock(Block):
    type = Identifier('candle_cake')
    def __init__(self, id:Identifier|str, cake:Identifier=Identifier('cake'), material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id)
        self.cake = cake

        # STATES

        self.lit = self.add_state(BooleanState(self.identifier.copy_with_path('lit')))

        # COMPONENTS
        self.add_component(LootComponent('loot_tables/blocks/black_candle.json'))
        self.add_component(GeometryComponent('geometry.template_cake_with_candle'))
        self.add_component(LightDampeningComponent(0))
        self.add_component(DestructibleByExplosionComponent(0.5))
        self.add_component(DestructibleByMiningComponent(0.5))
        self.add_component(OnInteractComponent())
        self.add_component(SelectionBoxComponent([-7,0,-7], [14,8,14]))
        self.add_component(CollisionBoxComponent([-7,0,-7], [14,8,14]))

        # PERMUTATIONS

        # EVENTS
        oi = Sequence()
        oi.set_condition(0, Molang(f"q.block_state('{ self.lit.id }') == false && q.is_item_name_any('slot.weapon.mainhand','minecraft:flint_and_steel')"))
        oi.add_event(0, SetBlockState({self.lit.id: 'true'}))
        oi.add_event(0, Damage('durability', 1, target=EventTarget.ITEM))
        oi.add_event(0, RunCommand('playsound fire.ignite @p ~ ~ ~ 1.0 1', EventTarget.BLOCK))
        oi.add_event(0, Trigger('flame'))
                
        oi.set_condition(1, Molang(f"q.block_state('{ self.lit.id }') == false && q.is_item_name_any('slot.weapon.mainhand','minecraft:fire_charge')"))
        oi.add_event(1, DecrementStack())
        oi.add_event(1, SetBlockState({self.lit.id: 'true'}))
        oi.add_event(1, RunCommand('playsound fire.ignite @p ~ ~ ~ 1.0 1'))
        oi.add_event(1, Trigger('flame'))
        
        oi.set_condition(2, Molang(f"q.block_state('{ self.lit.id }') == false && !q.is_item_name_any('slot.weapon.mainhand','minecraft:flint_and_steel') && !q.is_item_name_any('slot.weapon.mainhand','minecraft:fire_charge')"))
        oi.add_event(2, SpawnLoot('loot_tables/blocks/black_candle.json'))
        oi.add_event(2, RunCommand([f"setblock ~ ~ ~ {self.cake} [\"{ self.identifier.copy_with_path('bites') }\"=1]","playsound random.burp @p ~ ~ ~ 0.50","effect @s saturation 1 1 true"]))
        
        oi.set_condition(3, Molang(f"q.block_state('{ self.lit.id }') == true && !q.is_item_name_any('slot.weapon.mainhand','minecraft:flint_and_steel') && !q.is_item_name_any('slot.weapon.mainhand','minecraft:fire_charge')"))
        oi.add_event(3, SetBlockState({self.lit.id: 'false'}))
        oi.add_event(3, RunCommand('playsound random.fizz @p ~ ~ ~ 0.50', EventTarget.BLOCK))

        self.add_event('on_interact', oi)
        self.add_event('flame', RunCommand('particle minecraft:candle_flame_particle ~ ~0.5 ~', EventTarget.BLOCK))

class DoorBlock(Block):
    type = Identifier('door')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id, RenderMethod.ALPHA_TEST)
        self.add_trait(PlacementDirectionTrait.cardinal())

        # STATES

        self.open = self.add_state(BooleanState(self.identifier.copy_with_path('open')))
        self.half = self.add_state(BlockState(self.identifier.copy_with_path('half'), 'bottom', 'top'))

        # COMPONENTS

        self.add_component(OnInteractComponent())
        self.add_component(OnPlacedComponent(condition=Molang(f"q.block_state('{self.half}')=='bottom'")))

        # PERMUTATIONS
        perm1 = BlockPermutation(Molang("q.block_state('minecraft:cardinal_direction')=='north'"))
        perm1.add_component(TransformationComponent(rotation=[0,0,0]))
        self.add_permutation(perm1)
        
        perm2 = BlockPermutation(Molang("q.block_state('minecraft:cardinal_direction')=='south'"))
        perm2.add_component(TransformationComponent(rotation=[0,180,0]))
        self.add_permutation(perm2)
        
        perm3 = BlockPermutation(Molang("q.block_state('minecraft:cardinal_direction')=='east'"))
        perm3.add_component(TransformationComponent(rotation=[0,90,0]))
        self.add_permutation(perm3)
        
        perm4 = BlockPermutation(Molang("q.block_state('minecraft:cardinal_direction')=='west'"))
        perm4.add_component(TransformationComponent(rotation=[0,-90,0]))
        self.add_permutation(perm4)
        
        # EVENTS
        u = Sequence()
        i = 0
        for s in ['north', 'south', 'east', 'west']:
            for o in ['true', 'false']:
                u.set_condition(i, Molang(f"q.block_state('minecraft:cardinal_direction')=='{s}'&&q.block_state('{self.open}')=={o}"))
                u.add_event(i, RunCommand(f'execute if block ~ ~1 ~ {self.identifier} run setblock ~ ~1 ~ {self.identifier}[\"{self.half}\"=\"top\",\"minecraft:cardinal_direction\"=\"{s}\",\"{self.open}\"=\"{o}\"]'))
                i+=1
        self.add_event('on_update', u)

        self.add_event('on_interact', RunCommand('playsound use.stone @p', EventTarget.PLAYER))
        self.add_event('on_interact', SetBlockState({self.open.id: f"!q.block_state('{self.open}')"}))
        self.add_event('on_interact', Trigger('on_update'))

        self.add_event('on_placed', RunCommand(["execute unless block ~ ~1 ~ air run setblock ~ ~ ~ air destroy"]))
        self.add_event('on_placed', Trigger('on_update'))

class TrapdoorBlock(Block):
    type = Identifier('trapdoor')
    def __init__(self, id:Identifier|str, material: Material=None):
        Block.__init__(self, id, MenuCategory(Category.CONSTRUCTION, 'itemGroup.name.trapdoor'))
        if material is None: material = Material(id, RenderMethod.ALPHA_TEST)
        self.add_trait(PlacementDirectionTrait.cardinal())
        self.add_trait(PlacementPositionTrait.vertical_half())

        # STATES

        self.open = self.add_state(BooleanState(self.identifier.copy_with_path('open')))

        # COMPONENTS
        self.add_component(LootComponent(f'loot_tables/blocks/{self.identifier.path}.json'))
        self.add_component(SelectionBoxComponent([-8, 0, -8], [16, 3, 16]))
        self.add_component(CollisionBoxComponent([-8, 0, -8], [16, 3, 16]))
        mi = MaterialInstancesComponent()
        mi.add_material('*', Material('minecraft:stone') if material is None else material)
        self.add_component(mi)
        self.add_component(OnInteractComponent())

        # TODO PERMUTATIONS

        # EVENTS
        self.add_event('on_interact', RunCommand('playsound use.basalt @p', target=EventTarget.PLAYER))
        self.add_event('on_interact', SwitchBlockState(self.open.id))

class ButtonBlock(Block):
    type = Identifier('button')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id.replace('_button', ''))
        self.add_trait(PlacementDirectionTrait.facing())

        # STATES

        self.powered = self.add_state(BooleanState(self.identifier.copy_with_path('powered')))

        # COMPONENTS

        self.add_component(LootComponent(f'loot_tables/blocks/{self.identifier.path}.json'))
        self.add_component(OnInteractComponent())
        mi = MaterialInstancesComponent()
        mi.add_material('*', material)
        self.add_component(mi)

        # PERMUTATIONS

        perm1 = BlockPermutation(Molang("q.block_state('minecraft:facing_direction')=='north'"))
        perm1.add_component(TransformationComponent(rotation=[0,0,0]))
        self.add_permutation(perm1)
        
        perm2 = BlockPermutation(Molang("q.block_state('minecraft:facing_direction')=='south'"))
        perm2.add_component(TransformationComponent(rotation=[0,180,0]))
        self.add_permutation(perm2)
        
        perm3 = BlockPermutation(Molang("q.block_state('minecraft:facing_direction')=='east'"))
        perm3.add_component(TransformationComponent(rotation=[0,90,0]))
        self.add_permutation(perm3)
        
        perm4 = BlockPermutation(Molang("q.block_state('minecraft:facing_direction')=='west'"))
        perm4.add_component(TransformationComponent(rotation=[0,-90,0]))
        self.add_permutation(perm4)

        # EVENTS

        self.add_event('on_interact', SwitchBlockState(self.powered.id))

class PressurePlateBlock(Block):
    type = Identifier('pressure_plate')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id.replace('_pressure_plate', ''))

        # STATES

        self.triggered = self.add_state(BooleanState(self.identifier.copy_with_path('triggered')))
        self.powered = self.add_state(BooleanState(self.identifier.copy_with_path('powered')))

        # COMPONENTS

        self.add_component(OnStepOnComponent())
        self.add_component(OnStepOffComponent())
        self.add_component(QueuedTickingComponent([5,5], Trigger('unpower', Molang(f"q.block_state('{self.triggered}')==false&&q.block_state('{self.powered}')==true"))))

        # PERMUTATIONS

        perm1 = BlockPermutation(Molang(f"q.block_state('{self.powered}')==true"))
        perm1.add_component(GeometryComponent('geometry.template_pressure_plate.powered'))
        self.add_permutation(perm1)

        perm2 = BlockPermutation(Molang(f"q.block_state('{self.powered}')==false"))
        perm2.add_component(GeometryComponent('geometry.template_pressure_plate'))
        self.add_permutation(perm2)

        # EVENTS

        self.add_event('on_step_on', SetBlockState({self.powered.id: "true", self.triggered.id: "true"}))
        self.add_event('on_step_off', SetBlockState({self.triggered.id: "false"}))
        self.add_event('unpower', SetBlockState({self.powered.id: "false"}))

class CauldronBlock(Block):
    type = Identifier('cauldron')
    def __init__(self, id:Identifier|str, empty_bucket:Identifier|str=Identifier('bucket'), filled_bucket:Identifier|str=Identifier('lava_bucket'), material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id, RenderMethod.BLEND)

        # COMPONENTS

        self.add_component(OnInteractComponent(condition=Molang(f"q.is_item_name_any('slot.weapon.mainhand','{Identifier(empty_bucket)}')")))

        # EVENTS

        self.add_event('on_interact', DecrementStack())
        self.add_event('on_interact', RunCommand(f'give @s {Identifier(filled_bucket)}', target=EventTarget.PLAYER))

class CauldronLevelBlock(CauldronBlock):
    type = Identifier('cauldron_level')
    def __init__(self, id:Identifier|str, empty_bucket:Identifier|str=Identifier('bucket'), filled_bucket:Identifier|str=Identifier('water_bucket'), empty_bottle:Identifier|str=Identifier('glass_bottle'), filled_bottle:Identifier|str=Identifier('water_bottle'), material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id, RenderMethod.BLEND)
        # STATES
        
        self.level = self.add_state(IntegerState(self.identifier.copy_with_path('level'), 3))

        # COMPONENTS

        # TODO: For bucket check if level=3
        cond1 = Molang(f"q.is_item_name_any('slot.weapon.mainhand','{Identifier(empty_bucket)}')&&q.block_state('{self.level}')==3")
        cond2 = Molang(f"q.is_item_name_any('slot.weapon.mainhand','{Identifier(empty_bottle)}')&&q.block_state('{self.level}')>=1")

        self.add_component(OnInteractComponent(condition=Molang(f"({cond1})||({cond2})")))

        # TODO: PERMUTATIONS
        
        # EVENTS
        self.clear_events()
        oi = Sequence()
        oi.set_condition(0, cond1)
        oi.add_event(0, DecrementStack())
        oi.add_event(0, RunCommand(f'give @s {filled_bucket}', EventTarget.PLAYER))
        oi.add_event(0, SetBlockState({self.level.id: "0"}))

        oi.set_condition(1, cond2)
        oi.add_event(1, DecrementStack())
        oi.add_event(1, RunCommand(f'give @s {filled_bottle}', EventTarget.PLAYER))
        oi.add_event(1, DecrementBlockState(self.level.id))

        self.add_event('on_interact', oi)

class FenceBlock(Block):
    type = Identifier('fence')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id.replace('_fence', ''))

        # STATES

        self.north = self.add_state(BooleanState(self.identifier.copy_with_path('north')))
        self.east = self.add_state(BooleanState(self.identifier.copy_with_path('east')))
        self.south = self.add_state(BooleanState(self.identifier.copy_with_path('south')))
        self.west = self.add_state(BooleanState(self.identifier.copy_with_path('west')))
        states = [self.north, self.east, self.south, self.west]

        # COMPONENTS

        self.add_component(BlockTags([Identifier('fence')]))
        self.add_component(QueuedTickingComponent([1,1], Trigger('on_update')))
        self.add_component(BoneVisabilityComponent({
            'north': 'false',
            'east': 'false',
            'south': 'false',
            'west': 'false',
        }))

        # PERMUTATIONS

        for s in states:
            perm = BlockPermutation(Molang(f"q.block_state('{s}') == true"))
            perm.add_component(BlockTags([s.id]))
            self.add_permutation(perm)

        # EVENTS
        ou = Sequence()
        i = 0
        for s in self.states.values():
            ou.set_condition(i, Molang(f"q.block_state('{s}')==false&&q.block_neighbor_has_all_tags(0,1,0, '{Identifier('fence')}')"))
            ou.add_event(i, SetBlockState({s: "true"}))

            ou.set_condition(i+1, Molang(f"q.block_state('{s}')==true&&!q.block_neighbor_has_all_tags(0,1,0, '{Identifier('fence')}')"))
            ou.add_event(i+1, SetBlockState({s: "false"}))
            i+=2

        self.add_event('on_update', ou)

class FenceGateBlock(Block):
    type = Identifier('fence_gate')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id)
        self.add_trait(PlacementDirectionTrait.cardinal())
        if material is None: material = Material(id.replace('_fence_gate',''))

        # STATES

        self.open = self.add_state(BooleanState(self.identifier.copy_with_path('open')))

        # COMPONENTS

        self.add_component(BlockTags([Identifier('fence_gate')]))
        self.add_component(OnInteractComponent())

        # PERMUTATIONS

        perm1 = BlockPermutation(Molang(f"q.block_state('minecraft:cardinal_direction')=='north'"))
        perm1.add_component(TransformationComponent(rotation=[0,0,0]))
        self.add_permutation(perm1)

        perm2 = BlockPermutation(Molang(f"q.block_state('minecraft:cardinal_direction')=='south'"))
        perm2.add_component(TransformationComponent(rotation=[0,180,0]))
        self.add_permutation(perm2)
        
        perm3 = BlockPermutation(Molang(f"q.block_state('minecraft:cardinal_direction')=='east'"))
        perm3.add_component(TransformationComponent(rotation=[0,90,0]))
        self.add_permutation(perm3)
        
        perm4 = BlockPermutation(Molang(f"q.block_state('minecraft:cardinal_direction')=='west'"))
        perm4.add_component(TransformationComponent(rotation=[0,-90,0]))
        self.add_permutation(perm4)
        
        perm5 = BlockPermutation(Molang(f"q.block_state('{self.open}')==true"))
        perm5.add_component(GeometryComponent('geometry.template_fence_gate.open'))
        self.add_permutation(perm5)
        
        perm6 = BlockPermutation(Molang(f"q.block_state('{self.open}')==false"))
        perm6.add_component(GeometryComponent('geometry.template_fence_gate'))
        self.add_permutation(perm6)

        # EVENTS

        self.add_event('on_interact', SwitchBlockState(self.open.id))

class GlassPane(Block):
    type = Identifier('glass_pane')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id.replace('_glass_pane', ''), RenderMethod.BLEND)

        # STATES

        self.north = self.add_state(BooleanState(self.identifier.copy_with_path('north')))
        self.east = self.add_state(BooleanState(self.identifier.copy_with_path('east')))
        self.south = self.add_state(BooleanState(self.identifier.copy_with_path('south')))
        self.west = self.add_state(BooleanState(self.identifier.copy_with_path('west')))

        # COMPONENTS

        self.add_component(GeometryComponent('geometry.template_wall_post'))
        self.add_component(BlockTags([Identifier('glass_pane')]))
        self.add_component(QueuedTickingComponent([1, 1], Trigger('on_update')))
        self.add_component(BoneVisabilityComponent({
            'north_tall': 'false',
            'east_tall': 'false',
            'south_tall': 'false',
            'west_tall': 'false',
            'north': 'false',
            'east': 'false',
            'south': 'false',
            'west': 'false',
        }))

        # PERMUTATIONS

        for s in [self.north, self.east, self.south, self.west]:
            perm = BlockPermutation(Molang(f"q.block_state('{s}')==true"))
            perm.add_component(BoneVisabilityComponent({s.id.path: "true"}))
            self.add_permutation(perm)

        # EVENTS
            
        ou = Sequence()
        i = 0
        for s in self.states.values():
            ou.set_condition(i, Molang(f"q.block_state('{s}')==false&&q.block_neighbor_has_all_tags(0,1,0, '{Identifier('glass_pane')}')"))
            ou.add_event(i, SetBlockState({s: "true"}))

            ou.set_condition(i+1, Molang(f"q.block_state('{s}')==true&&!q.block_neighbor_has_all_tags(0,1,0, '{Identifier('glass_pane')}')"))
            ou.add_event(i+1, SetBlockState({s: "false"}))
            i+=2

        self.add_event('on_update', ou)

class LanternBlock(Block):
    type = Identifier('lantern')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id, RenderMethod.ALPHA_TEST)
        self.add_trait(PlacementPositionTrait.vertical_half())

        # COMPONENTS

        self.add_component(LightEmissionComponent(15))
        mi = MaterialInstancesComponent()
        mi.add_material('*', material)
        self.add_component(mi)

        # PERMUTATIONS

        perm1 = BlockPermutation(Molang(f"q.block_state('minecraft:vertical_half')=='top'"))
        perm1.add_component(GeometryComponent('geometry.template_hanging_lantern'))
        self.add_permutation(perm1)
        
        perm2 = BlockPermutation(Molang(f"q.block_state('minecraft:vertical_half')=='bottom'"))
        perm2.add_component(GeometryComponent('geometry.template_lantern'))
        self.add_permutation(perm2)

# TODO
class TorchBlock(Block):
    type = Identifier('torch')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id, RenderMethod.ALPHA_TEST)
        self.add_trait(PlacementDirectionTrait.facing())
        # TODO: "up" state should break the block (Illegal placement)

        # COMPONENTS

        # PERMUTATIONS

        # EVENTS

class WallBlock(Block):
    type = Identifier('wall')
    def __init__(self, id:Identifier|str, material:Material=None):
        Block.__init__(self, id)
        if material is None: material = Material(id.replace('_wall',''), RenderMethod.ALPHA_TEST)

        # STATES

        self.up = self.add_state(BooleanState(self.identifier.copy_with_path('up')))
        self.north = self.add_state(BooleanState(self.identifier.copy_with_path('north')))
        self.east = self.add_state(BooleanState(self.identifier.copy_with_path('east')))
        self.south = self.add_state(BooleanState(self.identifier.copy_with_path('south')))
        self.west = self.add_state(BooleanState(self.identifier.copy_with_path('west')))

        # COMPONENTS

        self.add_component(GeometryComponent('geometry.template_wall_post'))
        self.add_component(BlockTags([Identifier('wall')]))
        self.add_component(QueuedTickingComponent([1, 1], Trigger('on_update')))
        self.add_component(BoneVisabilityComponent({
            'north_tall': 'false',
            'east_tall': 'false',
            'south_tall': 'false',
            'west_tall': 'false',
            'north': 'false',
            'east': 'false',
            'south': 'false',
            'west': 'false',
        }))

        # PERMUTATIONS

        for s in [self.north, self.east, self.south, self.west]:
            perm = BlockPermutation(Molang(f"q.block_state('{s}')==true&&q.block_state('{self.up}')==true"))
            perm.add_component(BoneVisabilityComponent({s.id.path+'_tall': "true"}))
            self.add_permutation(perm)
            
            perm = BlockPermutation(Molang(f"q.block_state('{s}')==true&&q.block_state('{self.up}')==false"))
            perm.add_component(BoneVisabilityComponent({s.id.path: "true"}))
            self.add_permutation(perm)

        # EVENTS
            
        ou = Sequence()
        i = 0
        for s in self.states.values():
            ou.set_condition(i, Molang(f"q.block_state('{s}')==false&&q.block_neighbor_has_all_tags(0,1,0, '{Identifier('wall')}')"))
            ou.add_event(i, SetBlockState({s: "true"}))

            ou.set_condition(i+1, Molang(f"q.block_state('{s}')==true&&!q.block_neighbor_has_all_tags(0,1,0, '{Identifier('wall')}')"))
            ou.add_event(i+1, SetBlockState({s: "false"}))
            i+=2

        self.add_event('on_update', ou)
