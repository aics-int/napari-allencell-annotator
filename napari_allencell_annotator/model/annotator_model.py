class AnnotatorModel:
    def __init__(self):
        # Stores annotations, dictionary of Path -> dict of annotations key/value
        self._annotations: dict[Path, dict[str|any]] = dict()
