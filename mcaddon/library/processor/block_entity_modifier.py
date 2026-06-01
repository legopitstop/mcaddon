__all__ = ["BlockEntityModifier", "AppendLootBlockEntityModifier"]

from mcaddon.core.base import BaseTypedModel, TypedModel


class BlockEntityModifier(BaseTypedModel):
    pass


@BlockEntityModifier.register
class AppendLootBlockEntityModifier(TypedModel):
    TYPE_ID = "minecraft:append_loot"
    type: str = TYPE_ID

    loot_table: str
