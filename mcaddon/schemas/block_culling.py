import os

from .. import __file__, Schema, BlockCullingRules, CullingRule, GeometryPart


class BlockCullingRulesSchema1(Schema):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "block_culling1.json"
            ),
        )

    def load(cls, self: BlockCullingRules, data: dict):
        self.identifier = data["description"]["identifier"]

        for rule in data["rules"]:
            self.add_rule(CullingRule.from_dict(rule))
