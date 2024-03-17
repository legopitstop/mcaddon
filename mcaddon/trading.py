from typing import Self
import os

from .pack import behavior_pack
from .util import (
    getattr2,
    setattr2,
    getitem,
    additem,
    removeitem,
    clearitems,
    Identifier,
    Identifiable,
    Misc,
)
from .loot import LootFunction
from .file import JsonFile
from .math import Range


class TradeChoice:

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        return self

    def jsonify(self) -> dict:
        data = {}
        return data


# TODO: add choice
class ItemTrade(Misc):
    def __init__(
        self,
        item: Identifiable,
        quantity: int = None,
        choice: TradeChoice = None,
        functions: list[LootFunction] = None,
        price_multiplier: float = 0.0,
    ):
        self.item = item
        self.quantity = quantity
        self.price_multiplier = price_multiplier
        self.functions = functions

    def jsonify(self) -> dict:
        data = {"item": str(self.item)}
        if self.quantity is not None:
            if isinstance(self.quantity, Range):
                data["quantity"] = self.quantity.jsonify()
            else:
                data["quantity"] = self.quantity
        if self.price_multiplier:
            data["price_multiplier"] = self.price_multiplier
        if self.functions:
            data["functions"] = [x.jsonify() for x in self.functions]
        return data

    @property
    def functions(self) -> list[LootFunction]:
        return getattr2(self, "_functions", [])

    @functions.setter
    def functions(self, value: list[LootFunction]):
        setattr2(self, "_functions", value, list)

    @property
    def item(self) -> Identifier:
        return getattr(self, "_item", None)

    @item.setter
    def item(self, value: Identifiable):
        id = Identifiable.of(value)
        self.on_update("item", id)
        setattr(self, "_item", id)

    @property
    def quantity(self) -> int:
        return getattr(self, "_quantity", None)

    @quantity.setter
    def quantity(self, value: Range | int):
        if value is None:
            return
        if not isinstance(value, (Range, int)):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        self.on_update("quantity", value)
        setattr(self, "_quantity", value)

    @property
    def price_multiplier(self) -> float:
        return getattr(self, "_price_multiplier")

    @price_multiplier.setter
    def price_multiplier(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"Expected float but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_price_multiplier", value)

    @property
    def choice(self) -> TradeChoice:
        return getattr(self, "_choice")

    @choice.setter
    def choice(self, value: TradeChoice):
        if not isinstance(value, TradeChoice):
            raise TypeError(
                f"Expected TradeChoice but got '{value.__class__.__name__}' instead"
            )
        self.on_update("choice", value)
        setattr(self, "_choice", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "item" in data:
            self.item = data.pop("item")
        else:
            self.choice = TradeChoice.from_dict(data)

        if "quantity" in data:
            q = data.pop("quantity")
            if isinstance(q, dict):
                self.quantity = Range.from_dict(q)
            else:
                self.quantity = q

        if "price_multiplier" in data:
            self.price_multiplier = data.pop("price_multiplier")
        return self

    # FUNCTIONS

    def get_functions(self, index: int) -> LootFunction:
        return getitem(self, "functions", index)

    def add_function(self, trade: LootFunction) -> LootFunction:
        return additem(self, "functions", trade, type=LootFunction)

    def remove_function(self, index: int) -> LootFunction:
        return removeitem(self, "functions", index)

    def clear_functions(self) -> Self:
        """Remove all functions"""
        return clearitems(self, "functions")


class Trade(Misc):
    def __init__(
        self,
        wants: list[ItemTrade],
        gives: list[ItemTrade],
        max_uses: int,
        trader_exp: int = None,
        reward_exp: bool = True,
    ):
        self.wants = [wants] if isinstance(wants, ItemTrade) else wants
        self.gives = [gives] if isinstance(gives, ItemTrade) else gives
        self.max_uses = max_uses
        self.trader_exp = trader_exp
        self.reward_exp = reward_exp

    def jsonify(self) -> dict:
        data = {
            "wants": [i.jsonify() for i in self.wants],
            "gives": [i.jsonify() for i in self.gives],
        }
        if self.max_uses:
            data["max_uses"] = self.max_uses
        if self.trader_exp:
            data["trader_exp"] = self.trader_exp
        if self.reward_exp is not None:
            data["reward_exp"] = self.reward_exp
        return data

    @property
    def reward_exp(self) -> bool:
        return getattr(self, "_reward_exp")

    @reward_exp.setter
    def reward_exp(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f"Expected bool but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_reward_exp", value)

    @property
    def max_uses(self) -> int:
        return getattr(self, "_max_uses", None)

    @max_uses.setter
    def max_uses(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_max_uses", value)

    @property
    def trader_exp(self) -> int:
        return getattr(self, "_trader_exp", None)

    @trader_exp.setter
    def trader_exp(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_trader_exp", value)

    @property
    def wants(self) -> list[ItemTrade]:
        return getattr2(self, "_wants", [])

    @wants.setter
    def wants(self, value: list[ItemTrade]):
        if value is None:
            self.wants = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("wants", value)
        setattr(self, "_wants", value)

    @property
    def gives(self) -> list[ItemTrade]:
        return getattr2(self, "_gives", [])

    @gives.setter
    def gives(self, value: list[ItemTrade]):
        if value is None:
            self.gives = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("gives", value)
        setattr(self, "_gives", value)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.wants = [ItemTrade.from_dict(i) for i in data.pop("wants")]
        self.gives = [ItemTrade.from_dict(i) for i in data.pop("gives")]
        if "max_uses":
            self.max_uses = data.pop("max_uses")
        if "trader_exp":
            self.trader_exp = data.pop("trader_exp")
        if "reward_exp":
            self.reward_exp = data.pop("reward_exp")
        return self

    def get_want(self, index: int) -> ItemTrade:
        return getitem(self, "wants", index)

    def add_want(self, item: ItemTrade) -> ItemTrade:
        return additem(self, "wants", item, type=ItemTrade)

    def remove_want(self, index: int) -> ItemTrade:
        return removeitem(self, "wants", index)

    def clear_wants(self) -> Self:
        return clearitems(self, "wants")

    def get_give(self, index: int) -> ItemTrade:
        return getitem(self, "gives", index)

    def add_give(self, item: ItemTrade) -> ItemTrade:
        return additem(self, "gives", item, type=ItemTrade)

    def remove_give(self, index: int) -> ItemTrade:
        return removeitem(self, "gives", index)

    def clear_gives(self) -> Self:
        return clearitems(self, "gives")


class TradeGroup(Misc):
    def __init__(self, num_to_select: int, trades: list[Trade] = None):
        self.num_to_select = num_to_select
        self.trades = trades

    @property
    def num_to_select(self) -> int:
        return getattr(self, "_num_to_select")

    @num_to_select.setter
    def num_to_select(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_num_to_select", value)

    @property
    def trades(self) -> list[Trade]:
        return getattr2(self, "_trades", [])

    @trades.setter
    def trades(self, value: list[Trade]):
        setattr2(self, "_trades", value, list)

    @staticmethod
    def from_dict(data: dict) -> Self:
        num_to_select = data.pop("num_to_select")
        trades = [Trade.from_dict(x) for x in data.pop("trades")]
        return TradeGroup(num_to_select, trades)

    def jsonify(self) -> dict:
        data = {
            "num_to_select": self.num_to_select,
            "trades": [trade.jsonify() for trade in self.trades],
        }
        return data

    def get_trade(self, index: int) -> Trade:
        return getitem(self, "trades", index)

    def add_trade(self, trade: Trade) -> Trade:
        return additem(self, "trades", trade, type=Trade)

    def remove_trade(self, index: int) -> Trade:
        return removeitem(self, "trades", index)

    def clear_trades(self) -> Self:
        """Remove all trades"""
        return clearitems(self, "trades")


class TradeTier(Misc):
    def __init__(
        self,
        total_exp_required: int = None,
        trades: list[Trade] = None,
        groups: list[TradeGroup] = None,
    ):
        self.trades = trades
        self.groups = groups
        self.total_exp_required = total_exp_required

    def __iter__(self):
        for i in self.trades:
            yield i

    def jsonify(self) -> dict:
        data = {}
        if self.trades:
            data["trades"] = [i.jsonify() for i in self.trades]
        if self.groups:
            data["groups"] = [i.jsonify() for i in self.groups]
        if self.total_exp_required:
            data["total_exp_required"] = self.total_exp_required
        return data

    @property
    def total_exp_required(self) -> int:
        return getattr(self, "_total_exp_required", None)

    @total_exp_required.setter
    def total_exp_required(self, value: int):
        if value is None:
            return
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_total_exp_required", value)

    @property
    def groups(self) -> list[TradeGroup]:
        return getattr2(self, "_groups", [])

    @groups.setter
    def groups(self, value: list[TradeGroup]):
        if value is None:
            self.groups = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        setattr(self, "_groups", value)

    @property
    def trades(self) -> list[Trade]:
        return getattr2(self, "_trades", [])

    @trades.setter
    def trades(self, value: list[Trade]):
        if value is None:
            self.trades = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("trades", value)
        setattr(self, "_trades", value)

    # TRADES

    def get_trade(self, index: int) -> Trade:
        return getitem(self, "trades", index)

    def add_trade(self, trade: Trade) -> Trade:
        return additem(self, "trades", trade, type=Trade)

    def remove_trade(self, index: int) -> Trade:
        return removeitem(self, "trades", index)

    def clear_trades(self) -> Self:
        """Remove all trades"""
        return clearitems(self, "trades")

    # GROUPS

    def get_group(self, index: int) -> TradeGroup:
        return getitem(self, "groups", index)

    def add_group(self, group: TradeGroup) -> TradeGroup:
        return additem(self, "groups", group, type=TradeGroup)

    def remove_group(self, index: int) -> TradeGroup:
        return removeitem(self, "groups", index)

    def clear_group(self) -> Self:
        """Remove all groups"""
        return clearitems(self, "groups")

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        if "trades" in data:
            self.trades = [Trade.from_dict(i) for i in data.pop("trades")]
        if "groups" in data:
            self.groups = [TradeGroup.from_dict(x) for x in data.pop("groups")]
        return self


@behavior_pack
class Trading(JsonFile, Identifiable):
    """
    Represents a Trade Table.
    """

    id = Identifier("trading")
    FILEPATH = "trading/trade.json"

    def __init__(self, identiifer: Identifiable, tiers: list[TradeTier] = None):
        Identifiable.__init__(self, identiifer)
        self.tiers = tiers

    def __iter__(self):
        for i in self.tiers:
            yield i

    def __str__(self) -> str:
        return "Trading{" + repr(self.identifier.path) + "}"

    @property
    def tiers(self) -> list[TradeTier]:
        return getattr2(self, "_tiers", [])

    @tiers.setter
    def tiers(self, value: list[TradeTier]):
        if value is None:
            self.tiers = []
            return
        if not isinstance(value, list):
            raise TypeError(
                f"Expected list but got '{value.__class__.__name__}' instead"
            )
        self.on_update("tiers", value)
        setattr(self, "_tiers", value)

    def jsonify(self) -> dict:
        data = {"tiers": [i.jsonify() for i in self.tiers]}
        return data

    def valid(self, fp: str) -> bool:
        return True

    def get_tier(self, index: int) -> TradeTier:
        return getitem(self, "tiers", index)

    def add_tier(self, tier: TradeTier) -> TradeTier:
        return additem(self, "tiers", tier, type=TradeTier)

    def remove_tier(self, index: int) -> TradeTier:
        return removeitem(self, "tiers", index)

    def clear_tiers(self, index: int) -> Self:
        """Remove all trade tiers"""
        return clearitems(self, "tiers")

    @classmethod
    def open(cls, fp: str, start):
        with open(fp, "r") as fd:
            self = cls.load(fd)
            self.identifier = os.path.relpath(fp, start).replace("\\", "/")
            return self

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        self = cls.__new__(cls)
        self.tiers = [TradeTier.from_dict(i) for i in data.pop("tiers")]
        return self
