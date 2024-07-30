import json
from pathlib import Path

from napari_allencell_annotator.model.combo_key import ComboKey
from napari_allencell_annotator.model.key import Key


class JSONUtils:

    @staticmethod
    def dict_to_json_dump(annotation_keys: dict[str, Key]) -> str:
        # convert annotation_keys to json compatible format
        keys_dict: dict[str, dict] = {}
        for key, key_info in annotation_keys.items():
            keys_dict[key] = {
                "type": str(key_info.get_type()),
                "default": key_info.get_default_value(),
            }
            if isinstance(key_info, ComboKey):
                keys_dict[key]["options"] = key_info.get_options()
        return json.dumps(keys_dict)

    @staticmethod
    def json_dump_to_dict(json_data: str) -> dict[str, Key]:
        original_dict = json.loads(json_data)
        converted_dict: dict[str, Key] = {}
        for key, value in original_dict.items():
            # this means it is a combo_key
            if "options" in list(value.keys()):
                converted_dict[key] = ComboKey(value["type"], value["options"], value["default"])
            # is a Key
            else:
                converted_dict[key] = Key(value["type"], value["default"])

        return converted_dict

    @staticmethod
    def get_json_data(path: Path) -> str:
        with open(path, "r") as f:
            return f.read()

    @staticmethod
    def write_json_data(data: str, path: Path) -> None:
        with open(path, "w") as f:
            f.write(data)
