from typing import Literal
from .item import ItemData


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

    @staticmethod
    def func(name: str, arg: str | int) -> str:
        return "{%s(%s)}" % (name, arg)

    @staticmethod
    def opt_one(item_specifier: str | ItemData):
        return Requires.func(
            "OptOne",
            (
                item_specifier
                if isinstance(item_specifier, str)
                else item_specifier["name"]
            ),
        )

    @staticmethod
    def opt_all(input: str):
        return Requires.func("OptAll", input)

    @staticmethod
    def item_value(key: str, value: str | int):
        return Requires.func("ItemValue", f"{key}:{value}")

    @staticmethod
    def yaml_compare(option_name: str, op: str, value: str | int):
        return Requires.func("YamlCompare", f"{option_name} {op} {value}")
