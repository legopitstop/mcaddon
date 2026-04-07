__all__ = ["EntityBaseMovementComponent"]

from mcaddon.library.entity.component import EntityComponent


@EntityComponent.register
class EntityBaseMovementComponent(EntityComponent):
    max_turn: float = 30
