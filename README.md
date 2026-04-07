# mcaddon

![Tests](https://github.com/legopitstop/mcaddon/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/mcaddon)](https://pypi.org/project/mcaddon/)
[![Python](https://img.shields.io/pypi/pyversions/mcaddon)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/mcaddon)
![Status](https://img.shields.io/pypi/status/mcaddon)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/legopitstop/mcaddon)](https://github.com/legopitstop/mcaddon/issues)

Template python package.

## Installation

Install the module with pip:

```bat
pip3 install mcaddon
```

Update existing installation: `pip3 install mcaddon --upgrade`

## Requirements

| Name                                                 | Description                  |
| ---------------------------------------------------- | ---------------------------- |
| [`mini-racer`](https://pypi.org/project/mini-racer/) | JavaScript engine for Python |
| [`pillow`](https://pypi.org/project/pillow/)         | For handling images          |
| [`nbtlib`](https://pypi.org/project/nbtlib/)         | For reading/writing NBT      |

## Features

-

## Examples

### Block

```py
from mcaddon import *

block = Block()
block.description.identifier = "test:on_interact_change_state_block"
block.components.add(BlockGeometryComponent())
block.components.add(
    BlockMaterialInstancesComponent().add(MaterialInstance(texture="stone"))
)
block.components.add(BlockCollisionBoxComponent())
block.components.add(BlockSelectionBoxComponent())
block.save("block.json")
```

### Item

```py
from mcaddon import *

item = Item()
item.description.identifier = "minecraft:blaze_rod"
item.components.add(ItemFuelComponent(duration=12))
item.components.add(ItemMaxStackSizeComponent(value=64))
item.components.add(ItemIconComponent().add("blaze_rod"))
item.components.add(ItemHandEquippedComponent())
item.components.add(ItemDisplayNameComponent(value="Blaze Rod"))
item.save("item.json")
```

## Command-line interface

```
usage: mcaddon [-h] [-V]

Description

options:
  -h, --help     show this help message and exit
  -V, --version  print the mcaddon version number and exit.

```
