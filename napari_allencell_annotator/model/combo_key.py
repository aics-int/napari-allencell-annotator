from napari_allencell_annotator.model.key import Key


class ComboKey(Key):
    def __init__(self, key_name: str, type: type, dropdown_options: list[str], key_default_value: str = None):
        super().__init__(key_name, type, key_default_value)
        self._dropdown_options = dropdown_options

    def get_options(self) -> list[str]:
        return self._dropdown_options
