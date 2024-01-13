# mcaddon

[![PyPI](https://img.shields.io/pypi/v/mcaddon)](https://pypi.org/project/mcaddon/)
[![Python](https://img.shields.io/pypi/pyversions/mcaddon)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/mcaddon)
![Status](https://img.shields.io/pypi/status/mcaddon)
[![Issues](https://img.shields.io/github/issues/legopitstop/mcaddon)](https://github.com/legopitstop/mcaddon/issues)

Utility functions for creating Minecraft Bedrock Add-Ons.

## Installation

Install the module with pip:

```bat
pip3 install mcaddon
```

Update existing installation: `pip3 install mcaddon --upgrade`

## Examples

### Block

```Python
from mcaddon import *

blk = Block('test:on_interact_change_state_block')
blk.add_component(OnInteractComponent(event='test_event'))
blk.add_event('test_event', SetBlockState({'custom:direction': "1"}))
blk.save('block.json')
```

### Item

```Python
from mcaddon import *

blk = Item('minecraft:blaze_rod')
blk.add_component(FuelComponent(12.0))
blk.add_component(MaxStackSizeComponent(64))
blk.add_component(IconComponent('blaze_rod'))
blk.add_component(HandEquippedComponent(True))
blk.add_component(DisplayNameComponent('Blaze Rod'))
blk.save('item.json')
```

## Our Goal?

Our goal is to create a library that can create a mcpack from the ground up using Python.

## Road map

- Resource packs
  - [ ] animation_controllers/
  - [ ] animations/
  - [ ] biomes_client.json
  - [ ] blocks.json
  - [ ] cameras/
  - [ ] entity/
  - [ ] font/
  - [ ] materials/
  - [ ] models/
  - [ ] particles/
  - [ ] pieces/
  - [ ] render_controllers/
  - [ ] sounds/
  - [ ] sounds.json
  - [x] texts/
  - [ ] textures/
  - [ ] ui/
- Behavior packs
  - [x] blocks/
  - [ ] cameras/
  - [ ] entities/
  - [ ] feature_rules/
  - [ ] features/
  - [x] items/
  - [ ] loot_tables/
  - [ ] recipes/
  - [ ] spawn_rules/
  - [ ] structures/
  - [ ] texts/
  - [ ] trading/
- Skin packs
- Addons
- contents.json
