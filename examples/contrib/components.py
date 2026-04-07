from typing import ClassVar
from mcaddon import (
    BiomeComponent,
    SpawnRuleComponent,
)


# Register a custom component
@BiomeComponent.register
class MyComponent(BiomeComponent):
    COMPONENT_ID: ClassVar[str] = "minecraft:my_component"
    text: str


# print(BiomeComponent.__all__)
# print(BlockComponent.__all__)
# print(ClientBiomeComponent.__all__)
# print(EntityComponent.__all__)
# print(ItemComponent.__all__)
# print(ParticleComponent.__all__)
# print(SpawnRuleComponent.__all__)

for cls in SpawnRuleComponent.__all__.values():
    print(cls)
