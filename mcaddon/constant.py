from enum import Enum

__all__ = ['ModuleType','Category', 'RenderMethod','EventTarget', 'UseAnimation', 'RecipeTag','Color']

class ModuleType(Enum):
    RESOURCES='resources'
    DATA='data'
    CLIENT_DATA='client_data'
    INTERFACE='interface'
    WORLD_TEMPLATE='world_template'

class Category(Enum): # https://github.com/legopitstop/JSON-Schemas/blob/6381dc2087908b4956985530b78ef2c03999863e/schemas/bedrock/common.json#L357-L367
    COMMANDS='commands'
    CONSTRUCTION='construction'
    EQUIPMENT='equipment'
    ITEMS='items'
    NATURE='nature'
    NONE='none'

class RenderMethod(Enum): # https://github.com/legopitstop/JSON-Schemas/blob/6381dc2087908b4956985530b78ef2c03999863e/schemas/bedrock/behavior/block.json#L33-L36
    OPAQUE='opaque'
    DOUBLE_SIDED='double_sided'
    BLEND='blend'
    ALPHA_TEST='alpha_test'

class EventTarget(Enum): # https://github.com/legopitstop/JSON-Schemas/blob/6381dc2087908b4956985530b78ef2c03999863e/schemas/bedrock/common.json#L373-L382
    SELF='self'
    HOLDER='holder'
    BABY='baby'
    OTHER='other'
    PLAYER='player'
    TARGET='target'
    PARENT='parent'
    BLOCK='block'
    DAMAGER='damager'
    ITEM='item'

class UseAnimation(Enum): # https://github.com/legopitstop/JSON-Schemas/blob/6381dc2087908b4956985530b78ef2c03999863e/schemas/bedrock/common.json#L420-L422
    EAT='eat'
    DRINK='drink'
    CAMERA='camera'

class RecipeTag(Enum): # https://github.com/legopitstop/JSON-Schemas/blob/6381dc2087908b4956985530b78ef2c03999863e/schemas/bedrock/common.json#L429-L436
    FURNACE='furnace'
    SMOKER='smoker'
    CAMPFIRE='campfire'
    SOUL_CAMPFIRE='soul_campfire'
    CRAFTING_TABLE='crafting_table'
    BREWING_STAND='brewing_stand'
    STONECUTTER='stonecutter'
    SMITHING_TABLE='smithing_table'

class BlockFace(Enum): # https://github.com/legopitstop/JSON-Schemas/blob/6381dc2087908b4956985530b78ef2c03999863e/schemas/bedrock/behavior/block.json#L48-L55
    UP='up'
    DOWN='down'
    NORTH='north'
    SOUTH='south'
    EAST='east'
    WEST='west'
    SIDE='side'
    ALL='all'

class Color(Enum):
    WHITE='white'
    LIGHT_GRAY='light_gray'
    GRAY='gray'
    BLACK='black'
    BROWN='brown'
    RED='red'
    ORANGE='orange'
    YELLOW='yellow'
    LIME='lime'
    GREEN='green'
    CYAN='cyan'
    LIGHT_BLUE='light_blue'
    BLUE='blue'
    PURPLE='purple'
    MAGENTA='magenta'
    PINK='pink'

