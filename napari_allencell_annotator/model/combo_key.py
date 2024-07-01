from napari_allencell_annotator.model.key import Key


class ComboKey(Key):
    def __init__(self, type: type, dropdown_options: list[str],  key_default_value: str = None):
        super().__init__("list", key_default_value)
        self._dropdown_options = dropdown_options

    def get_options(self) -> list[str]:
        return self._dropdown_options

