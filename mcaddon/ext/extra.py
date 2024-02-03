"""
Custom BlockTraits and BlockComponents
"""

from ..block import block_trait, BlockTrait, BlockComponent
from ..loot import LootTable, LootContextType
from ..util import Identifier

# BLOCK TRAITS
#  - StrongRedstonePowerTrait - a BooleanState which will be modified when the block is being powered
#  - WeakRedstonePowerTrait - which will be modified baised on the redstone signal level.

# BLOCK COMPONENT
# OnNeighborUpdate - Only updates when a new block has been placed nearby
