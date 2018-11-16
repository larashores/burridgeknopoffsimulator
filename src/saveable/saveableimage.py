import io
from PIL import Image

from saveable.saveabletype import SaveableType
from saveable.saveableint import U32


class SaveableImage(SaveableType):
    """
    A Saveable image type that can hold PIL images
    """
    def __init__(self, image=None):
        self._image = image

    def set(self, value):
        if not isinstance(value, Image.Image):
            raise ValueError('{} is not an image type'.format(value))
        self._image = value

    def get(self):
        return self._image

    def load_in_place(self, byte_array, index=0):
        size, index = U32.from_byte_array(byte_array, index)
        stream = io.BytesIO(byte_array)
        self._image = Image.open(stream)
        self._image.load()
        stream.close()
        return index + size.value

    def to_byte_array(self):
        _bytes = io.BytesIO()
        self._image.save(_bytes, format=self._image.format if self._image.format is not None else 'PNG')
        size = U32()
        size.set(len(_bytes.getvalue()))
        return size.to_byte_array() + bytearray(_bytes.getvalue())

