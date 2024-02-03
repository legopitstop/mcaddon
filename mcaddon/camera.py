from typing import Self

from . import VERSION
from .constant import CameraListener
from .file import JsonFile, Loader
from .util import Identifier, Identifiable


class CameraPreset(JsonFile, Identifiable):
    """
    Represents a Camera Preset.
    """

    id = Identifier("camera_preset")
    EXTENSION = ".json"
    FILENAME = "camera_preset"
    DIRNAME = "cameras"

    def __init__(
        self,
        identifier: Identifier | str,
        inherit_from: Identifier = None,
        player_effects: bool = False,
        pos_x: int = None,
        pos_y: int = None,
        pos_z: int = None,
        rot_x: int = None,
        rot_y: int = None,
        listener: CameraListener = None,
    ):
        Identifiable.__init__(self, identifier)
        self.inherit_from = inherit_from
        self.player_effects = player_effects
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.rot_x = rot_x
        self.rot_y = rot_y
        self.listener = listener

    def __str__(self) -> str:
        return "CameraPreset{" + str(self.identifier) + "}"

    @property
    def __dict__(self) -> dict:
        camera = {"description": {"identifier": str(self.identifier)}}
        if self.inherit_from:
            camera["inherit_from"] = self.inherit_from
        if self.player_effects:
            camera["player_effects"] = self.player_effects
        if self.pos_x:
            camera["pos_x"] = self.pos_x
        if self.pos_y:
            camera["pos_y"] = self.pos_y
        if self.pos_z:
            camera["pos_z"] = self.pos_z
        if self.rot_x:
            camera["rot_x"] = self.rot_x
        if self.rot_y:
            camera["rot_y"] = self.rot_y
        if self.listener not in [None, CameraListener.none]:
            camera["listener"] = self.listener._value_
        data = {"format_version": VERSION["ITEM"], str(self.id): camera}
        return data

    @property
    def inherit_from(self) -> Identifier:
        return getattr(self, "_inherit_from", None)

    @inherit_from.setter
    def inherit_from(self, value: Identifier):
        if value is None:
            setattr(self, "_inherit_from", None)
            return
        if not isinstance(value, Identifier):
            raise TypeError(
                f"Expected Identifier but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_inherit_from", value)

    @property
    def player_effects(self) -> bool:
        return getattr(self, "_player_effects", False)

    @player_effects.setter
    def player_effects(self, value: bool):
        if value is None:
            self.player_effects = False
            return
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_player_effects", value)

    @property
    def pos_x(self) -> int:
        return getattr(self, "_pos_x", None)

    @pos_x.setter
    def pos_x(self, value: int):
        if value is None:
            setattr(self, "_pos_x", None)
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_pos_x", value)

    @property
    def pos_y(self) -> int:
        return getattr(self, "_pos_y", None)

    @pos_y.setter
    def pos_y(self, value: int):
        if value is None:
            setattr(self, "_pos_y", None)
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_pos_y", value)

    @property
    def pos_z(self) -> int:
        return getattr(self, "_pos_z", None)

    @pos_z.setter
    def pos_z(self, value: int):
        if value is None:
            setattr(self, "_rot_z", None)
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_pos_z", value)

    @property
    def rot_x(self) -> int:
        return getattr(self, "_rot_x", None)

    @rot_x.setter
    def rot_x(self, value: int):
        if value is None:
            setattr(self, "_rot_x", None)
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_rot_x", value)

    @property
    def rot_y(self) -> int:
        return getattr(self, "_rot_y", None)

    @rot_y.setter
    def rot_y(self, value: int):
        if value is None:
            setattr(self, "_rot_y", None)
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_rot_y", value)

    @property
    def listener(self) -> CameraListener:
        return getattr(self, "_listener", CameraListener.none)

    @listener.setter
    def listener(self, value: CameraListener):
        if value is None:
            self.listener = CameraListener.none
        elif isinstance(value, CameraListener):
            setattr(self, "_listener", value)
        else:
            self.listener = CameraListener[value]

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = CameraPresetLoader()
        loader.validate(data)
        return loader.load(data)


class CameraPresetLoader(Loader):
    name = "Camera"

    def __init__(self):
        from .schemas import CameraPresetSchem1

        Loader.__init__(self, CameraPreset)
        self.add_schema(CameraPresetSchem1, "1.20.51")
