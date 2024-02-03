# mcaddon

[![PyPI](https://img.shields.io/pypi/v/mcaddon)](https://pypi.org/project/mcaddon/)
[![Python](https://img.shields.io/pypi/pyversions/mcaddon)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/mcaddon)
![Status](https://img.shields.io/pypi/status/mcaddon)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/legopitstop/mcaddon)](https://github.com/legopitstop/mcaddon/issues)

Utility functions for creating Minecraft Bedrock Add-Ons.

Documentation: https://mcaddon.readthedocs.io/

## Installation

Install the module with pip:

```bat
pip3 install mcaddon
```

Update existing installation: `pip3 install mcaddon --upgrade`

## Requirements

| Name | Description |
|--|--|
| [`mclang`](https://pypi.org/project/mclang/) | Read and write to .lang files. |
| [`molang`](https://pypi.org/project/molang/) | Molang to Python Translator & interpreter written in pure Python. |
| [`commentjson`](https://pypi.org/project/commentjson/) | Add Python and JavaScript style comments in your JSON files. |
| [`jsonschema`](https://pypi.org/project/jsonschema/) | An implementation of JSON Schema validation for Python |
| [`chevron`](https://pypi.org/project/chevron/) | Mustache templating language renderer |

## Our Goal?

Our goal is to create a library that can create a mcaddon or mcpack from the ground up using Python.

## Features
- Load packs from any format version.
- Supports [mustache](https://mustache.github.io/) logic-less templates.

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

## Command-line interface
```
```

## Road map

- Resource packs
  - [ ] animation_controllers
  - [ ] animations
  - [ ] attachables
  - [ ] biomes_client.json
  - [ ] blocks.json
  - [ ] cameras
  - [ ] entity
  - [ ] flipbook_textures.json
  - [ ] font
  - [ ] item_textures.json
  - [ ] materials
  - [ ] models
  - [ ] particles
  - [ ] pieces
  - [ ] render_controllers
  - [ ] sounds
  - [ ] sounds.json
  - [ ] terrain_textures.json
  - [ ] texture set
  - [ ] textures
  - [ ] ui
  - [x] texts
- Behavior packs
  - [ ] cameras
  - [ ] entities
  - [ ] feature_rules
  - [ ] features
  - [ ] spawn_rules
  - [ ] structures
  - [ ] trading
  - [x] blocks
  - [x] items
  - [x] loot_tables
  - [x] recipes
  - [x] texts
  - [x] volume
- Skin packs
- [x] Addons
- contents.json
- cli
   - update mcaddon/mcpack
- Support to load all format versions. (At least all versions that are used in vanilla packs)
- Support to import packs. (for both singleplayer and on dedicated server)
- Toolchain to load packs
- scripting - Convert Python to the Official Minecraft [Scripting and API](https://learn.microsoft.com/en-us/minecraft/creator/scriptapi/minecraft/server/minecraft-server?view=minecraft-bedrock-stable).
