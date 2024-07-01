from typing import Any


class Key:
    def __init__(self, key_name: str, type: type, key_default_value: Any = None) -> None:
        self._key_name = str
        self._type: type = type
        self._key_default_value = key_default_value

    def get_key_name(self) -> str:
        return self._key_name

    def get_type(self) -> type:
        return self._type

    def get_default_value(self) -> Any:
        return self._key_default_value
