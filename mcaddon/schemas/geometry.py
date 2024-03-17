import os

from .. import __file__, INSTANCE, Schema, Geometry, EntityModel


class GeometrySchema1(Schema):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "geometry1.json"
            ),
        )

    def load(cls, self: Geometry, data: dict):
        for x in data:
            model = EntityModel.from_dict(x)
            self.add_model(model)
