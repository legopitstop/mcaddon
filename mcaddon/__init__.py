"""
Minecraft: Bedrock Edition development kit
"""

import os
import sys

__version__ = "0.0.2"

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
    "MANIFEST": 1,
    "BLOCK": "1.20.51",
    "BLOCKS": "1.16.220",
    "ITEM": "1.20.51",
    "VOLUME": "1.20.50",
    "MIN_ENGINE_VERSION": [1, 20, 51],
}

from .exception import *
from .registry import *
from .constant import *
from .file import *
from .util import *

from .manifest import *
from .resrouce import *
from .pack import *
from .event import *
from .loot import *
from .block import *
from .state import *
from .item import *
from .recipe import *
from .volume import *
from .camera import *

# from .animation import *
# from .biome import *
# from .entity import *
# from .feature import *
# from .fog import *
# from .particle import *
# from .texture_set import *
# from .volume import *
