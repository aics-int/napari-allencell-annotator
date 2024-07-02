from typing import Any


class Key:
<<<<<<< HEAD
    def __init__(self, key_name: str, type: type, key_default_value: Any = None) -> None:
        self._key_name = str
        self._type: type = type
=======
    def __init__(self, type: str, key_default_value: Any = None) -> None:
        self._type: str = type
>>>>>>> refactor-base
        self._key_default_value = key_default_value

    def get_type(self) -> str:
        return self._type

    def get_default_value(self) -> Any:
        return self._key_default_value
