import io
import cairosvg
from PIL import Image, ImageTk


class SvgLoader:
    """Utility class for loading and caching SVG images as Tkinter-compatible PhotoImage objects."""
    def __init__(self):
        self.cache = {}

    def load(self, path: str, size: int):
        """Loads an SVG file, converts it to a Tkinter-compatible image, and caches it for future use."""
        key = (path, size)

        if key not in self.cache:
            png_data = cairosvg.svg2png(
                url=path,
                output_width=size,
                output_height=size
            )

            image = Image.open(io.BytesIO(png_data))
            self.cache[key] = ImageTk.PhotoImage(image)

        return self.cache[key]
