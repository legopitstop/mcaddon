from .. import Schema, Manifest, Header, Metadata, Module, Dependency


class ManifestSchema1(Schema):
    def __init__(self):
        Schema.__init__(self, "schema11.json")

    def load(cls, self: Manifest, data: dict):
        if "header" in data:
            self.header = Header.from_dict(data["header"])
        if "metadata" in data:
            self.metadata = Metadata.from_dict(data["metadata"])

        if "dependencies" in data:
            for d in data["dependencies"]:
                dep = Dependency.from_dict(d)
                self.dependencies[dep.uuid] = dep

        if "modules" in data:
            for m in data["modules"]:
                module = Module.from_dict(m)
                self.modules[module.uuid] = module
