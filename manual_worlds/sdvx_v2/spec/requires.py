from typing import Literal
from .types import CategoryData, ItemData


class Requires:
    type Amount = int | str | Literal["all"] | Literal["half"]

    @staticmethod
    def item(item_specifier: str | ItemData, amount: Amount | None = None) -> str:
        item_name = (
            item_specifier
            if isinstance(item_specifier, str)
            else item_specifier["name"]
        )
        result = f"|{item_name}"

        if amount != None:
            result += f":{amount}"

        return result + "|"

    @staticmethod
    def category(category_name: str, amount: Amount | None = None) -> str:
        result = f"|@{category_name}"

        if amount != None:
            result += f":{amount}"

        return result + "|"

    @staticmethod
    def all_of(*specifiers: str) -> str:
        return "(" + " and ".join(specifiers) + ")"

    @staticmethod
    def any_of(*specifiers: str) -> str:
        return "(" + " or ".join(specifiers) + ")"
