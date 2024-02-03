from .. import (
    INSTANCE,
    Schema,
    Identifier,
    Registries,
    ComponentNotFoundError,
    EventNotFoundError,
    Item,
)


class ItemSchema1(Schema):
    def __init__(self):
        Schema.__init__(self, "item1.json")

    def load(cls, self: Item, data: dict):
        if "description" in data:
            desc = data["description"]
            if "identifier" in desc:
                self.identifier = desc["identifier"]

        if "components" in data:
            comp = data["components"]
            for k, v in comp.items():
                id = Identifier(k)
                clazz = INSTANCE.get_registry(Registries.ITEM_COMPONENT_TYPE).get(id)
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


class ItemSchema2(Schema):
    def __init__(self):
        Schema.__init__(self, "item2.json")

    def load(cls, self: Item, data: dict):
        if "description" in data:
            desc = data["description"]
            if "identifier" in desc:
                self.identifier = desc["identifier"]

        if "components" in data:
            comp = data["components"]
            for k, v in comp.items():
                id = Identifier(k)
                clazz = INSTANCE.get_registry(Registries.ITEM_COMPONENT_TYPE).get(id)
                if clazz is None:
                    raise ComponentNotFoundError(repr(id))
                self.components[id] = clazz.from_dict(v)
