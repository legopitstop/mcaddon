import os

from .. import (
    __file__,
    INSTANCE,
    Schema,
    BlockPermutation,
    Identifier,
    Registries,
    ComponentNotFoundError,
    EventNotFoundError,
    Block,
    BlockTagsComponent,
)


class BlockSchema1(Schema):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(os.path.dirname(__file__), "data", "schemas", "block1.json"),
        )

    def load(cls, self: Block, data: dict):
        self.identifier = data["description"]["identifier"]

        if "components" in data:
            comp = data["components"]
            tags = BlockTagsComponent()
            for k, v in comp.items():
                id = Identifier(k)
                if str(id).startswith("tag:"):
                    tags.add_tag(id.path)
                    continue
                clazz = INSTANCE.get_registry(Registries.BLOCK_COMPONENT_TYPE).get(id)
                if clazz is None:
                    raise ComponentNotFoundError(repr(id))
                self.components[id] = clazz.from_dict(v)

            # Add tag
            if len(tags.tags) >= 1:
                self.components[Identifier("tags")] = tags

        if "permutations" in data:
            for perm in data["permutations"]:
                self.permutations.append(BlockPermutation.from_dict(perm))

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
