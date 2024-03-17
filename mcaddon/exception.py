from .constant import Edition


class RegistryError(Exception): ...


class Error(Exception): ...


class ComponentNotFoundError(Error): ...


class EventNotFoundError(Error): ...


class SchemaNotFoundError(Error): ...


class TypeNotFoundError(Error): ...


class SyntaxError(Error): ...


class ManifestNotFoundError(Error): ...


class MinecraftNotFoundError(Error):
    def __init__(self, edition: Edition):
        if not isinstance(edition, Edition):
            raise TypeError(
                f"Expected Edition but got '{edition.__class__.__name__}' instead"
            )
        Error.__init__(self, repr(edition._value_))
