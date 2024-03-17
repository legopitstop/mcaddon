from .. import *
from .. import __file__


class FeatureRuleSchem1(Schema):
    def __init__(self):
        Schema.__init__(
            self,
            os.path.join(
                os.path.dirname(__file__), "data", "schemas", "feature_rules1.json"
            ),
        )

    def load(cls, self: FeatureRule, data: dict):
        self.identifier = data["description"]["identifier"]
        self.places_feature = data["description"]["places_feature"]
