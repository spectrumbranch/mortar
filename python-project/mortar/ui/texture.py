from typing import Optional

from mktech.validate import ensure_type
import OpenGL.GL as gl

from mortar.image import Image
from .. import log


class Texture:
    def __init__(self, image: Optional[Image] = None) -> None:
        if image is None:
            self.im: Optional[Image] = None
            self.size = (0, 0)
            self.gl_texture = None
        else:
            self.im = image
            self.size = image.size
            self.gl_texture = self._create_gl_texture(self.im.mode)

    def pixels(self) -> bytes:
        return ensure_type(self.im, Image).tobytes()

    def _create_gl_texture(self, mode: str) -> int:
        if self.im is None:
            assert False

        # save texture state
        last_texture = gl.glGetIntegerv(gl.GL_TEXTURE_BINDING_2D)

        (width, height) = self.im.size

        rgb = self.im.copy().convert('RGB')

        pixels = rgb.tobytes()
        # pixels = list(self.im.getdata())
        log.debug(f'{self.im.mode} w {width} h {height} {606 * 277 * 3}'
                  f' {len(pixels)} num px {len(list(pixels))}')
        # print(pixels)

        gl_texture: int = gl.glGenTextures(1)

        # gl.glPixelStorei(gl.GL_UNPACK_ROW_LENGTH, width * 3)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, gl_texture)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                           gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                           gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S,
                           gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T,
                           gl.GL_CLAMP_TO_EDGE)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height, 0,
                        gl.GL_RGB, gl.GL_UNSIGNED_BYTE, pixels)

        gl.glBindTexture(gl.GL_TEXTURE_2D, last_texture)

        return gl_texture

    @classmethod
    def from_file(cls, path: str) -> 'Texture':
        im = Image.open(path)

        return cls(im)
