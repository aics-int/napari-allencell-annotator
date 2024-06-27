from pathlib import Path

class AnnotatorModel:
    def __init__(self):
        # Stores annotations, dictionary of Path -> dict of annotations key/value
        self._annotations: dict[Path, dict[str|any]] = dict()
        self._added_images: list[Path] = [] # list of paths of added images
    def add_image(self, file_item: Path) -> None:
        self._added_images.append(file_item)

    def get_all_images(self) -> list[Path]:
        return self._added_images

    def get_num_images(self) -> int:
        return len(self._added_images)

    def set_all_images(self, list_of_img: list[Path]) -> None:
        self._added_images = list_of_img

    def remove_image(self, item: Path) -> None:
        self._added_images.remove(item)
    #
    # def set_shuffled_images(self, list_of_img: list[Path]) -> None:
    #     self._shuffled_images = list_of_img
    #
    # def get_shuffled_images(self) -> list[Path]:
    #     return self._shuffled_images

