import os

from .. import (
    __file__,
    INSTANCE,
    Schema,
    Identifier,
    Registries,
    ComponentNotFoundError,
    EventNotFoundError,
)


class VolumeSchema1(Schema):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(os.path.dirname(__file__), "data", "schemas", "volume1.json"),
        )

    def load(cls, self, data: dict):
        self.identifier = data["description"]["identifier"]

        if "components" in data:
            comp = data["components"]
            for k, v in comp.items():
                id = Identifier(k)
                clazz = INSTANCE.get_registry(Registries.VOLUME_COMPONENT_TYPE).get(id)
                if clazz is None:
                    raise ComponentNotFoundError(repr(id))
                self.components[id] = clazz.from_dict(v)

        if "events" in data:
            for k, v in data["events"].items():
                name = Identifier(k)
                for kk, vv in v.items():
                    id = Identifier(kk)
                    clazz = INSTANCE.get_registry(Registries.EVENT_TYPE).get(id)
                    if clazz is None:
                        raise EventNotFoundError(repr(id))
                    if id not in self.events:
                        self.events[name] = {}
                    self.events[name][id] = clazz.from_dict(vv)
