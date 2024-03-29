from typing import Self, Any

from .registry import INSTANCE, Registries
from .util import (
    getitem,
    additem,
    removeitem,
    clearitems,
    Identifier,
    Identifiable,
    Misc,
)


class BlockProperty(Misc):
    def __init__(self, *values: str, id: Identifiable = None):
        """
        Base state class for blocks

        :param id: The identifier of this blockstate, defaults to None
        :type id: Identifiable, optional
        """
        if id:
            self.id = id
        self.values = list(values)

    def __repr__(self) -> str:
        return "BlockProperty{" + str(self.id) + "}"

    def __str__(self) -> str:
        return str(self.id)

    def __iter__(self):
        for v in self.values:
            yield v

    @property
    def id(self) -> Identifier:
        return getattr(self, "_id")

    @id.setter
    def id(self, value: Identifiable):
        setattr(self, "_id", Identifiable.of(value))

    @property
    def values(self) -> list:
        return getattr(self, "_values", [])

    @values.setter
    def values(self, value: list):
        def _default(o):
            if isinstance(o, bool):
                return o
            elif isinstance(o, (int, float)):
                return o
            else:
                return str(o)

        if value is None:
            self.values = []
        elif isinstance(value, list):
            v = [_default(x) for x in value]
            self.on_update("values", v)
            setattr(self, "_values", v)
        else:
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )

    def get_value(self, index: int) -> Any:
        return getitem(self, "values", index)

    def add_value(self, value: Any) -> Any:
        return additem(self, "values", value)

    def remove_value(self, index: int) -> Any:
        return removeitem(self, "values", index)

    def clear_values(self) -> Self:
        """Remove all values"""
        return clearitems(self, "values")

    @classmethod
    def from_dict(cls, data: list) -> Self:
        self = cls.__new__(cls)
        return self

    def jsonify(self) -> list:
        data = {str(self.id): [x for x in self.values]}
        return data

    def default(self) -> str | int:
        """
        Get the default value for this block property
        """
        return self.values[0]


# STATES

INSTANCE.create_registry(Registries.BLOCK_STATE, BlockProperty)


def state(cls):
    """
    Add this state to the parser
    """

    def wrapper():
        if not issubclass(cls, BlockProperty):
            raise TypeError(f"Expected BlockProperty but got '{cls.__name__}' instead")
        return INSTANCE.register(Registries.BLOCK_STATE, cls.id, cls)

    return wrapper()


# BASES


class BooleanState(BlockProperty):
    def __init__(self, id: Identifiable = None, default: bool = False):
        """
        True or False blockstate

        :param id: The identifier of this blockstate, defaults to None
        :type id: Identifiable, optional
        :param default: The default value, defaults to None
        :type default: bool, optional
        """
        values = [True, False] if default else [False, True]
        BlockProperty.__init__(self, *values, id=id)


class IntegerState(BlockProperty):
    def __init__(self, stop: int, start: int = 0, id: Identifiable = None):
        """
        Integer blockstate from START to END

        :param stop: The maximum value
        :type stop: int
        :param start: The minimum value, defaults to 0
        :type start: int, optional
        :param id: The identifier of this blockstate, defaults to None
        :type id: Identifiable, optional
        """
        BlockProperty.__init__(self, *range(start, stop + 1), id=id)


# VANILLA


@state
class BlockFaceState(BlockProperty):
    id = Identifier("block_face")

    def __init__(self):
        """
        States: ["down", "up", "north", "south", "east", "west"]
        """
        BlockProperty.__init__(self, "down", "up", "north", "south", "east", "west")


@state
class VerticalHalfState(BlockProperty):
    id = Identifier("vertical_half")

    def __init__(self):
        """
        States: ["bottom", "up"]
        """
        BlockProperty.__init__(self, "bottom", "up")


@state
class CardinalDirectionState(BlockProperty):
    id = Identifier("cardinal_direction")

    def __init__(self):
        """
        States: ["north", "south", "east", "west"]
        """
        BlockProperty.__init__(self, "north", "south", "east", "west")


@state
class FacingDirectionState(BlockProperty):
    id = Identifier("facing_direction")

    def __init__(self):
        """
        States: ["down", "up", "north", "south", "east", "west"]
        """
        BlockProperty.__init__(self, "down", "up", "north", "south", "east", "west")


@state
class ActiveState(BooleanState):
    id = Identifier("active")

    def __init__(self):
        BooleanState.__init__(self)


@state
class AgeState(IntegerState):
    id = Identifier("age")

    def __init__(self):
        IntegerState.__init__(self, 15)


@state
class AgeBitState(BooleanState):
    id = Identifier("age_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class AllowUnderwaterBitState(BooleanState):
    id = Identifier("allow_underwater_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class AttachedBitState(BooleanState):
    id = Identifier("attached_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class AttachmentState(BlockProperty):
    id = Identifier("attachment")

    def __init__(self):
        BlockProperty.__init__(self, "standing", "hanging", "side", "multiple")


@state
class BambooLeafSizeState(BlockProperty):
    id = Identifier("bamboo_leaf_size")

    def __init__(self):
        BlockProperty.__init__(self, "no_leaves", "small_leaves", "large_leaves")


@state
class BambooStalkThicknessState(BlockProperty):
    id = Identifier("bamboo_stalk")

    def __init__(self):
        BlockProperty.__init__(self, "thin", "thick")


@state
class BigDripleafTiltState(BlockProperty):
    id = Identifier("bigt_dripleaf_tilt")

    def __init__(self):
        BlockProperty.__init__(self, "none", "unstable", "partial_tilt", "full_tilt")


@state
class BiteCounterState(IntegerState):
    id = Identifier("bite_counter")

    def __init__(self):
        IntegerState.__init__(self, 6)


@state
class BooksStoredState(IntegerState):
    id = Identifier("books_stored")

    def __init__(self):
        IntegerState.__init__(self, 6)


@state
class BrewingStandSlotABitState(BooleanState):
    id = Identifier("brewing_stand_slot_a_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class BrewingStandSlotBBitState(BooleanState):
    id = Identifier("brewing_stand_slot_b_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class BrewingStandSlotCBitState(BooleanState):
    id = Identifier("brewing_stand_slot_c_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class BrushedProgressState(IntegerState):
    id = Identifier("brushed_progress")

    def __init__(self):
        IntegerState.__init__(self, 3)


@state
class ButtonPressedBitState(BooleanState):
    id = Identifier("button_pressed_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class CandlesState(IntegerState):
    id = Identifier("candles")

    def __init__(self):
        IntegerState.__init__(self, 3)


@state
class CauldronLiquidState(BlockProperty):
    id = Identifier("cauldron_liquid")

    def __init__(self):
        BlockProperty.__init__(self, "water", "lava")


@state
class ChemistryTableTypeState(BlockProperty):
    id = Identifier("chemistry_table_type")

    def __init__(self):
        BlockProperty.__init__(
            self,
            "compound_creator",
            "material_reducer",
            "element_constructor",
            "lab_table",
        )


@state
class ChiselTypeState(BlockProperty):
    id = Identifier("chisel_type")

    def __init__(self):
        BlockProperty.__init__(self, "default", "chiseled", "lines", "smooth")


@state
class ClusterCountState(IntegerState):
    id = Identifier("cluster_count")

    def __init__(self):
        IntegerState.__init__(self, 3)


@state
class ColorState(BlockProperty):
    id = Identifier("color")

    def __init__(self):
        BlockProperty.__init__(
            self,
            "white",
            "orange",
            "magenta",
            "light_blue",
            "yellow",
            "lime",
            "pink",
            "gray",
            "silver",
            "cyan",
            "purple",
            "blue",
            "brown",
            "green",
            "red",
            "black",
        )


@state
class ColorBitState(BooleanState):
    id = Identifier("color_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class ConditionalBitState(BooleanState):
    id = Identifier("conditional_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class CoralColorState(BlockProperty):
    id = Identifier("coral_color")

    def __init__(self):
        BlockProperty.__init__(
            self,
            "blue",
            "pink",
            "purple",
            "red",
            "yellow",
            "blue",
            "blue dead",
            "pink dead",
            "red dead",
            "yelliow dead",
        )


@state
class CoralDirectionState(IntegerState):
    id = Identifier("coral_direction")

    def __init__(self):
        IntegerState.__init__(self, 3)


@state
class CoralHangTypeBitState(BooleanState):
    id = Identifier("coral_hang_type_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class CoveredBitState(BooleanState):
    id = Identifier("coverted_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class CrackedState(BlockProperty):
    id = Identifier("cracked_state")

    def __init__(self):
        BlockProperty.__init__(self, "no_cracks", "cracked", "max_cracked")


@state
class CraftingState(BooleanState):
    id = Identifier("crafting")

    def __init__(self):
        BooleanState.__init__(self)


@state
class DamageState(BlockProperty):
    id = Identifier("damage")

    def __init__(self):
        BlockProperty.__init__(
            self, "undamaged", "slightly_damaged", "very_damaged", "broken"
        )


@state
class DeadBitState(BooleanState):
    id = Identifier("dead_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class DirectionState(IntegerState):
    id = Identifier("direction")

    def __init__(self):
        IntegerState.__init__(self, 3)


@state
class DirtTypeState(BlockProperty):
    id = Identifier("dirt_type")

    def __init__(self):
        BlockProperty.__init__(self, "normal", "coarse")


@state
class DisarmedBitState(BooleanState):
    id = Identifier("disarmed_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class DoorHingeBitState(BooleanState):
    id = Identifier("door_hinge_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class DoublePlantTypeState(BlockProperty):
    id = Identifier("double_plant_type")

    def __init__(self):
        BlockProperty.__init__(
            self, "sunflower", "syringa", "grass", "fern", "rose", "paeonia"
        )


@state
class DragDownState(BooleanState):
    id = Identifier("drag_down")

    def __init__(self):
        BooleanState.__init__(self)


@state
class DripstoneThicknessState(BlockProperty):
    id = Identifier("dripstone_thickness")

    def __init__(self):
        BlockProperty.__init__(self, "tip", "frustum", "base", "middle", "merge")


@state
class EndPortalEyeBitState(BooleanState):
    id = Identifier("end_portal_eye_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class ExplodeBitState(BooleanState):
    id = Identifier("explode_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class FillLevelState(IntegerState):
    id = Identifier("fill_level")

    def __init__(self):
        IntegerState.__init__(self, 6)


@state
class FlowerTypeState(BlockProperty):
    id = Identifier("flower_type")

    def __init__(self):
        BlockProperty.__init__(
            self,
            "poppy",
            "orchid",
            "allium",
            "houstonia",
            "tulip_red",
            "tulip_orange",
            "tulip_white",
            "tulip_pink",
            "oxeye",
            "cornflower",
            "lily_of_the_valley",
        )


@state
class GroundSignDirectionState(IntegerState):
    id = Identifier("ground_sign_direction")

    def __init__(self):
        IntegerState.__init__(self, 15)


@state
class GrowthState(IntegerState):
    id = Identifier("growth")

    def __init__(self):
        IntegerState.__init__(self, 7)


@state
class HangingState(BooleanState):
    id = Identifier("hanging")

    def __init__(self):
        BooleanState.__init__(self)


@state
class HeadPieceBitState(BooleanState):
    id = Identifier("head_piece_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class HeightState(IntegerState):
    id = Identifier("height")

    def __init__(self):
        IntegerState.__init__(self, 7)


@state
class HugeMushroomBitsState(IntegerState):
    id = Identifier("huge_mushroom_bit")

    def __init__(self):
        IntegerState.__init__(self, 15)


@state
class InWallBitState(BooleanState):
    id = Identifier("in_wall_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class InfiniburnBitState(BooleanState):
    id = Identifier("infiniburn_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class ItemFrameMapBitState(BooleanState):
    id = Identifier("item_frame_map_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class ItemFramePhotoBitState(BooleanState):
    id = Identifier("item_frame_photo_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class LiquidDepthState(IntegerState):
    id = Identifier("liquid_depth")

    def __init__(self):
        IntegerState.__init__(self, 15)


@state
class MoisturizedAmountState(IntegerState):
    id = Identifier("moisturized_amount")

    def __init__(self):
        IntegerState.__init__(self, 7)


@state
class MonsterEggStoneTypeState(BlockProperty):
    id = Identifier("monster_egg_stone_type")

    def __init__(self):
        BlockProperty.__init__(
            self,
            "stone",
            "cobblestone",
            "stone_brick",
            "mossy_stone_brick",
            "cracked_stone_brick",
            "chiseled_stone_brick",
        )


@state
class NewLeafTypeState(BlockProperty):
    id = Identifier("new_leaf_type")

    def __init__(self):
        BlockProperty.__init__(self, "acacia", "dark_oak")


@state
class NewLogTypeState(BlockProperty):
    id = Identifier("new_log_type")

    def __init__(self):
        BlockProperty.__init__(self, "acacia", "dark_oak")


@state
class NoDropBitState(BooleanState):
    id = Identifier("no_drop_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class OccupiedBitState(BooleanState):
    id = Identifier("occupied_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class OldLeafTypeState(BlockProperty):
    id = Identifier("old_leaf_type")

    def __init__(self):
        BlockProperty.__init__(self, "oak", "spruce", "birch", "jungle")


@state
class OldLogTypeState(BlockProperty):
    id = Identifier("old_log_type")

    def __init__(self):
        BlockProperty.__init__(self, "oak", "spruce", "birch", "jungle")


@state
class OpenBitState(BooleanState):
    id = Identifier("open_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class OrientationState(BooleanState):
    id = Identifier("orientation")

    def __init__(self):
        BooleanState.__init__(self)


@state
class OutputLitBitState(BooleanState):
    id = Identifier("output_lit_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class OutputSubtractBitState(BooleanState):
    id = Identifier("output_subtract_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class PersistentBitState(BooleanState):
    id = Identifier("persistent_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class PortalAxisState(BlockProperty):
    id = Identifier("portal_axis")

    def __init__(self):
        BlockProperty.__init__(self, "unknown", "x", "z")


@state
class PoweredBitState(BooleanState):
    id = Identifier("powered_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class RailDataBitState(BooleanState):
    id = Identifier("rail_data_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class RailDirectionState(IntegerState):
    id = Identifier("rail_direction")

    def __init__(self):
        IntegerState.__init__(self, 8)


@state
class RedstoneSignalState(IntegerState):
    id = Identifier("redstone_signal")

    def __init__(self):
        IntegerState.__init__(self, 15)


@state
class RepeaterDelayState(IntegerState):
    id = Identifier("repeater_delay")

    def __init__(self):
        IntegerState.__init__(self, 3)


@state
class SandStoneTypeState(BlockProperty):
    id = Identifier("sand_stone_type")

    def __init__(self):
        BlockProperty.__init__(self, "default", "heiroglyphs", "cut", "smooth")


@state
class SandTypeState(BlockProperty):
    id = Identifier("sand_type")

    def __init__(self):
        BlockProperty.__init__(self, "normal", "type")


@state
class SaplingTypeState(BlockProperty):
    id = Identifier("sapling_type")

    def __init__(self):
        BlockProperty.__init__(
            self, "evergreen", "birch", "jungle", "acacia", "roofed_oak"
        )


@state
class SculkSensorPhaseState(BlockProperty):
    id = Identifier("sculk_sensor_phase")

    def __init__(self):
        BlockProperty.__init__(self, "inactive", "active", "cooldown")


@state
class SeaGrassTypeState(BlockProperty):
    id = Identifier("sea_grass_type")

    def __init__(self):
        BlockProperty.__init__(self, "default", "double_top", "double_bot")


@state
class SpongeTypeState(BlockProperty):
    id = Identifier("sponge_type")

    def __init__(self):
        BlockProperty.__init__(self, "dry", "wet")


@state
class StabilityState(IntegerState):
    id = Identifier("stability")

    def __init__(self):
        IntegerState.__init__(self, 5)


@state
class StabilityCheckState(BooleanState):
    id = Identifier("stability_check")

    def __init__(self):
        BooleanState.__init__(self)


@state
class StoneBrickTypeState(BlockProperty):
    id = Identifier("stone_brick_type")

    def __init__(self):
        BlockProperty.__init__(
            self, "default", "mossy", "cracked", "chiseled", "smooth"
        )


@state
class StoneSlabTypeState(BlockProperty):
    id = Identifier("stone_slab_type")

    def __init__(self):
        BlockProperty.__init__(
            self,
            "smooth_stone",
            "sandstone",
            "wood",
            "cobblestone",
            "brick",
            "stone_brick",
            "quartz",
            "nether_brick",
        )


@state
class StoneSlabType2State(BlockProperty):
    id = Identifier("stone_slab_type2")

    def __init__(self):
        BlockProperty.__init__(
            self,
            "red_sandstone",
            "purpur",
            "prismarine_rough",
            "prismarine_dark",
            "prismarine_brick",
            "mossy_cobblestone",
            "smooth_sandstone",
            "red_nether_brick",
        )


@state
class StoneSlabType3State(BlockProperty):
    id = Identifier("stone_slab_type3")

    def __init__(self):
        BlockProperty.__init__(
            self,
            "end_stone_brick",
            "smooth_red_sandstone",
            "polishe_andesite",
            "andesite",
            "diorite",
            "polished_diorite",
            "granite",
            "polished_granite",
        )


@state
class StoneSlabType4State(BlockProperty):
    id = Identifier("stone_slab_type_4")

    def __init__(self):
        BlockProperty.__init__(
            self,
            "mossy_stone_brick",
            "smooth_quartz",
            "stone",
            "cut_sandstone",
            "cut_red_sandstone",
        )


@state
class StoneTypeState(BlockProperty):
    id = Identifier("stone_type")

    def __init__(self):
        BlockProperty.__init__(
            self,
            "stone",
            "granite",
            "granite_smooth",
            "diorite",
            "diorite_smooth",
            "andesite",
            "andesite_smooth",
        )


@state
class StrippedBitState(BooleanState):
    id = Identifier("stripped_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class StructureBlockTypeState(BlockProperty):
    id = Identifier("structure_block_type")

    def __init__(self):
        BlockProperty.__init__(
            self, "data", "save", "load", "corner", "invalid", "export"
        )


@state
class StructureVoidTypeState(BlockProperty):
    id = Identifier("structure_void_type")

    def __init__(self):
        BlockProperty.__init__(self, "void", "air")


@state
class SuspendedBitState(BooleanState):
    id = Identifier("suspended_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class TallGrassTypeState(BlockProperty):
    id = Identifier("tall_grass_type")

    def __init__(self):
        BlockProperty.__init__(self, "default", "tall", "fern", "snow")


@state
class ToggleBitState(BooleanState):
    id = Identifier("toggle_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class TopSlotBitState(BooleanState):
    id = Identifier("top_slot_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class TorchFacingDirectionState(BlockProperty):
    id = Identifier("torch_facing_direction")

    def __init__(self):
        BlockProperty.__init__(self, "unknown", "west", "east", "north", "south", "top")


@state
class TriggedBitState(BooleanState):
    id = Identifier("triggered_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class TurtleEggCountState(BlockProperty):
    id = Identifier("turtle_egg_count")

    def __init__(self):
        BlockProperty.__init__(self, "one_egg", "two_egg", "three_egg", "four_egg")


@state
class UpdateBitState(BooleanState):
    id = Identifier("update_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class UpperBlockBitState(BooleanState):
    id = Identifier("upper_block_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class UpsideDownBitState(BooleanState):
    id = Identifier("upside_down_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class VineDirectionBitsState(IntegerState):
    id = Identifier("vine_direction_bits")

    def __init__(self):
        IntegerState.__init__(self, 15)


@state
class WallBlockTypeState(BlockProperty):
    id = Identifier("wall_block_type")

    def __init__(self):
        BlockProperty.__init__(
            self,
            "cobblestone",
            "mossy_cobblestone",
            "granite",
            "diorite",
            "andesite",
            "sandstone",
            "brick",
            "stone_brick",
            "mossy_stone_brick",
            "nether_brick",
            "end_brick",
            "prismarine",
            "red_sandstone",
            "red_nether_brick",
        )


@state
class WallConnectionTypEastState(BlockProperty):
    id = Identifier("wall_connection_type_east")

    def __init__(self):
        BlockProperty.__init__(self, "none", "short", "tall")


@state
class WallConnectionTypeNorthState(BlockProperty):
    id = Identifier("wall_connection_type_north")

    def __init__(self):
        BlockProperty.__init__(self, "none", "short", "tall")


@state
class WallConnectionTypeSouthState(BlockProperty):
    id = Identifier("wall_connection_type_south")

    def __init__(self):
        BlockProperty.__init__(self, "none", "short", "tall")


@state
class WallConnectionTypeWestState(BlockProperty):
    id = Identifier("wall_connection_type_west")

    def __init__(self):
        BlockProperty.__init__(self, "none", "short", "tall")


@state
class WallPostBitState(BooleanState):
    id = Identifier("wall_post_bit")

    def __init__(self):
        BooleanState.__init__(self)


@state
class WeirdoDirectionState(IntegerState):
    id = Identifier("weirdo_direction")

    def __init__(self):
        IntegerState.__init__(self, 3)


@state
class WoodTypeState(BlockProperty):
    id = Identifier("wood_type")

    def __init__(self):
        BlockProperty.__init__(
            self, "oak", "spruce", "birch", "jungle", "acacia", "dark_oak"
        )
