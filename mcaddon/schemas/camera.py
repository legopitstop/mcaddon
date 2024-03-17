import os

from .. import __file__, INSTANCE, Schema, CameraPreset


class CameraPresetSchem1(Schema):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(os.path.dirname(__file__), "data", "schemas", "camera1.json"),
        )

    def load(cls, self: CameraPreset, data: dict):
        self.identifier = data["identifier"]

        if "inherit_from" in data:
            self.inherit_from = data.pop("inherit_from")
        if "player_effects" in data:
            self.player_effects = data.pop("player_effects")
        if "pos_x" in data:
            self.pos_x = data.pop("pos_x")
        if "pos_y" in data:
            self.pos_y = data.pop("pos_y")
        if "pos_z" in data:
            self.pos_z = data.pop("pos_z")
        if "rot_x" in data:
            self.rot_x = data.pop("rot_x")
        if "rot_y" in data:
            self.rot_y = data.pop("rot_y")
        if "listener" in data:
            self.listener = data.pop("listener")
