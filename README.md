# mcaddon

![Tests](https://github.com/legopitstop/mcaddon/actions/workflows/tests.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/mcaddon)](https://pypi.org/project/mcaddon/)
[![Python](https://img.shields.io/pypi/pyversions/mcaddon)](https://www.python.org/downloads//)
![Downloads](https://img.shields.io/pypi/dm/mcaddon)
![Status](https://img.shields.io/pypi/status/mcaddon)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Issues](https://img.shields.io/github/issues/legopitstop/mcaddon)](https://github.com/legopitstop/mcaddon/issues)

Utility functions for creating Minecraft Bedrock Add-Ons.

## Installation

Install the module with pip:

```bat
pip3 install mcaddon
```

Update existing installation: `pip3 install mcaddon --upgrade`

## Requirements

| Name                                                     | Usage                                         |
| -------------------------------------------------------- | --------------------------------------------- |
| [`mini-racer`](https://pypi.org/project/mini-racer/)     | JavaScript engine for Python                  |
| [`pillow`](https://pypi.org/project/pillow/)             | Handling images                               |
| [`rapidnbt`](https://pypi.org/project/rapidnbt/)         | Reading/writing NBT                           |
| [`pydantic`](https://pypi.org/project/pydantic/)         | Data validation                               |
| [`mcpath`](https://pypi.org/project/mcpath/)             | Paths to Minecraft bedrock folders            |
| [`mclang`](https://pypi.org/project/mclang/)             | Read/write to .lang files                     |
| [`molang`](https://pypi.org/project/molang/)             | Molang translator & interpreter               |
| [`commentjson`](https://pypi.org/project/commentjson/)   | Reading JSON files with comments              |
| [`watchdog`](https://pypi.org/project/watchdog/)         | Monitor file system changes                   |
| [`Deprecated`](https://pypi.org/project/Deprecated/)     | Deprecated files and functions                |
| [`context_menu`](https://pypi.org/project/context_menu/) | Install context menus using<br>`mcaddon install` |

## Features

- Create Minecraft Bed rock add-ons with Python.
- Build behavior packs and resource packs.
- Define custom blocks and items.
- Use a modular, component based system.
- Export to Minecraft JSON files.
- Load and edit existing packs.
- Generate content with templates.
- Tools for managing and packaging add-ons.
- Optional scripting and integrations.

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
usage: mcaddon [-h] [-V] {show,logviewer,install,uninstall,package} ...

Description

positional arguments:
  {show,logviewer,install,uninstall,package}
    show                Shows a GUI for cli tools.
    logviewer           Opens the log viewer.
    install             Install context menu items.
    uninstall           Uninstall context menu items.
    package             Package a pack or world.

options:
  -h, --help            show this help message and exit
  -V, --version         print the mcaddon version number and exit.
```
