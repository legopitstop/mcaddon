__version__ = "1.0.0a1"
__format_version__ = "1.26.0"

from .core import *
from .library import *
import os
import mclang

ASSETS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")

mclang.init(os.path.join(ASSETS_PATH, "texts"))
