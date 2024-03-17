from typing import Self

from . import VERSION
from .constant import CameraListener
from .file import JsonFile, Loader
from .util import Identifier, Identifiable
from .pack import behavior_pack


@behavior_pack
class CameraPreset(JsonFile, Identifiable):
    """
    Represents a Camera Preset.
    """

    id = Identifier("camera_preset")
    FILEPATH = "cameras/presets/camera_preset.json"

    def __init__(
        self,
        identifier: Identifiable,
        inherit_from: Identifiable = None,
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
    def inherit_from(self) -> Identifier:
        return getattr(self, "_inherit_from", None)

    @inherit_from.setter
    def inherit_from(self, value: Identifiable):
        if value is None:
            setattr(self, "_inherit_from", None)
            return
        self.on_update("inherit_from", value)
        setattr(self, "_inherit_from", Identifiable.of(value))

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
        self.on_update("player_effects", value)
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
        self.on_update("pos_x", value)
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
        self.on_update("pos_y", value)
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
        self.on_update("pos_z", value)
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
        self.on_update("rot_x", value)
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
        self.on_update("rot_y", value)
        setattr(self, "_rot_y", value)

    @property
    def listener(self) -> CameraListener:
        return getattr(self, "_listener", CameraListener.NONE)

    @listener.setter
    def listener(self, value: CameraListener):
        if value is None:
            self.listener = CameraListener.NONE
        elif isinstance(value, CameraListener):
            self.on_update("listener", value)
            setattr(self, "_listener", value)
        else:
            self.listener = CameraListener(value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        loader = CameraPresetLoader()
        loader.validate(data)
        return loader.load(data)

    def jsonify(self) -> dict:
        camera = {"identifier": str(self.identifier)}
        if self.inherit_from is not None:
            camera["inherit_from"] = str(self.inherit_from)
        if self.player_effects is not None:
            camera["player_effects"] = self.player_effects
        if self.pos_x is not None:
            camera["pos_x"] = self.pos_x
        if self.pos_y is not None:
            camera["pos_y"] = self.pos_y
        if self.pos_z is not None:
            camera["pos_z"] = self.pos_z
        if self.rot_x is not None:
            camera["rot_x"] = self.rot_x
        if self.rot_y is not None:
            camera["rot_y"] = self.rot_y
        if self.listener not in [None, CameraListener.NONE]:
            camera["listener"] = self.listener.jsonify()
        data = {"format_version": VERSION["CAMERA"], str(self.id): camera}
        return data

    def position(self, x: int = 0, y: int = 0, z: int = 0) -> Self:
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z
        return self

    def rotation(self, x: int = 0, y: int = 0) -> Self:
        self.rot_x = x
        self.rot_y = y
        return self


class CameraPresetLoader(Loader):
    name = "Camera"

    def __init__(self):
        from .schemas import CameraPresetSchem1

        Loader.__init__(self, CameraPreset)
        self.add_schema(CameraPresetSchem1, "1.20.50")
        self.add_schema(CameraPresetSchem1, "1.19.50")
