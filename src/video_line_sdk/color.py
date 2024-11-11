from typing import Union


class Color:
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"
    WHITE = "#FFFFFF"
    BLACK = "#000000"

    def __init__(self, color: Union[str, "Color"]):
        if isinstance(color, Color):
            self.hex = color.hex
        else:
            if not color.startswith("#"):
                raise ValueError("Color must start with #")
            if len(color) != 7:
                raise ValueError("Color must be in #RRGGBB format")
            self.hex = color

    @property
    def rgb(self):
        return [int(self.hex[i : i + 2], 16) for i in (1, 3, 5)]
