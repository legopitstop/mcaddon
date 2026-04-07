# TODO: Move to mcaddon.core.base
__all__ = ["Number", "Vector3", "Vector2", "HexColor", "RGBA"]

from molang.dsl import MolangExpr
from typing import Tuple, Annotated
from pydantic import StringConstraints

Number = float | int

RGBA = (
    str
    | Tuple[float | MolangExpr, float | MolangExpr, float | MolangExpr]
    | Tuple[
        float | MolangExpr, float | MolangExpr, float | MolangExpr, float | MolangExpr
    ]
)
Vector3 = Tuple[Number, Number, Number]
Vector2 = Tuple[Number, Number]
HexColor = Annotated[
    str,
    StringConstraints(
        pattern=r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$"
    ),
]
