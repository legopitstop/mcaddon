"""
Minecraft: Bedrock Edition development kit
"""

import os
import sys

__version__ = "0.0.4"

# Unused for now
if sys.platform == "win32":
    APPDATA_PATH = os.path.expandvars(
        "%LocalAppData%\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
    )
    PRE_APPDATA_PATH = os.path.expandvars(
        "%LocalAppData%\\Packages\\Microsoft.MinecraftWindowsBeta_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
    )
    EDU_APPDATA_PATH = os.path.expandvars(
        "%LocalAppData%\\Packages\\Microsoft.MinecraftEducationEdition_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
    )
else:
    # Support more platforms
    # - ChromeOS - Python Shell Chrome Extension
    # - Linux - preinstalled
    # - iOS & iPadOS - Pythonista, Pyto
    # - Android - QPython, PyDroid, Python for Android
    # - Xbox - XBMC Python
    # - PS5 - ?
    # - Switch - nx-python
    # - FireOS - QPython, PyDroid, Python for Android
    APPDATA_PATH = None
    PRE_APPDATA_PATH = None
    EDU_APPDATA_PATH = None

VERSION = {
    "MANIFEST": 2,
    "BLOCK": "1.20.50",
    "BLOCK_CULLING_RULES": "1.20.60",
    "BLOCKS": "1.16.220",
    "ITEM": "1.20.50",
    "VOLUME": "1.20.50",
    "CAMERA": "1.20.50",
    "RECIPE": "1.20.50",
    "FEATURE": "1.16.0",
    "FEATURE_RULE": "1.12",
    "GEOMETRY": "1.12.0",
    "MIN_ENGINE_VERSION": [1, 20, 51],
}

from .exception import *
from .registry import *
from .constant import *
from .file import *
from .math import *
from .util import *
from .predicate import *

from .pack import *
from .text import *
from .resrouce import *
from .manifest import *

# ResourcePack
from .geometry import *

# from .client_entity import *
# from .particle import *
# from .material import *
# from .render_controller import *
# from .ui import *
# from .client_item import *
# from .piece import *
# from .animation_controllers import *
# from .animation import *
# from .camera_entity import *
# from . import *
# from . import *

# BehaviorPack
from .event import *
from .loot import *
from .state import *
from .block import *
from .block_culling import *
from .item import *
from .recipe import *
from .volume import *
from .camera import *
from .trading import *
from .feature import *
from .feature_rule import *

# from .entity import *
# from .behavior_tree import *
# from .spawn_rule import *
# from .structure import *

# SkinPack
# from .skin import *
