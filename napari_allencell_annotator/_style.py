from napari_allencell_annotator.util.directories import Directories


class Style:
    cache = dict()

    @classmethod
    def get_stylesheet(cls, name: str) -> str:
        if name is None:
            raise ValueError("Stylesheet name can't be None")
        if not name.endswith(".qss"):
            raise ValueError("Stylesheet must be a qss file (.qss)")

        if name not in cls.cache:
            cls.cache[name] = cls._load_from_file(name)

        return cls.cache[name]

    @classmethod
    def _load_from_file(cls, name: str) -> str:
        path = str(Directories.get_style_dir() / name)
        with open(path, "r") as handle:
            return handle.read()
