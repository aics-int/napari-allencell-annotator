from typing import Any


class Key:
    def __init__(self, type: str, key_default_value: Any = None) -> None:
        self._type: str = type
        self._key_default_value = key_default_value

    def get_type(self) -> str:
        return self._type

    def get_default_value(self) -> Any:
        return self._key_default_value
