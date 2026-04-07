from mcaddon import Version, BaseModel


class ExampleScheme(BaseModel):
    version: Version


def test_version():
    result = ExampleScheme.model_validate({"version": (1, 0, 0)})
    assert result.model_dump()["version"] == (1, 0, 0), result
