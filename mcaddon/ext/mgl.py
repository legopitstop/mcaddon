# Support for moderngl
from typing import Self
import moderngl
import os

from .. import __file__, Model


# https://stackoverflow.com/questions/44384543/how-to-render-3d-object-to-silhouette-image-in-python
class MGLRenderer:
    def __init__(self, ctx: moderngl.Context = None, size: tuple = (512, 512)):
        # def __init__(self, ctx:moderngl.Context=None, size:tuple=(2000, 2000)):
        self.size = size
        self.vbo = None
        self.fbo = None
        self.ctx = moderngl.create_standalone_context() if ctx is None else ctx

        with open(
            os.path.join(os.path.dirname(__file__), "data", "shaders", "default.vert")
        ) as fd:
            vertex_shader = fd.read()

        with open(
            os.path.join(os.path.dirname(__file__), "data", "shaders", "default.frag")
        ) as fd:
            fragment_shader = fd.read()

        self.program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        self.program["m_proj"].write(self.get_camera_projection_matrix())
        self.program["m_view"].write(self.get_camera_view_matrix())

    def render(self, model: Model) -> Self:
        self.program["m_model"].write(model.get_matrix())

        vao = self.ctx.vertex_array(
            self.program,
            [
                (
                    self.ctx.buffer(model.get_vertex_data()),
                    "3f 3f",
                    "in_normal",
                    "in_position",
                )
            ],
            skip_errors=True,
        )
        self.fbo = self.ctx.framebuffer(self.ctx.renderbuffer(self.size))
        self.fbo.use()

        self.ctx.viewport = (0, 0, self.size[0], self.size[1])
        self.ctx.clear(0.9, 0.9, 0.9)
        vao.render()

        # pixels = fbo.read(components=3, alignment=1)
        # return Image.frombytes("RGB", fbo.size, pixels).transpose(Image.FLIP_TOP_BOTTOM)
        return self

    def get_camera_view_matrix(self):
        import glm

        pos = glm.vec3((0, 0, 0))
        up = glm.vec3(0, 1, 0)
        forward = glm.vec3(0, 0, -1)
        return glm.lookAt(pos, pos + forward, up)

    def get_camera_projection_matrix(self):
        import glm

        FOV = 50
        NEAR = 0.1
        FAR = 200
        return glm.perspective(glm.radians(FOV), self.size[0] / self.size[1], NEAR, FAR)
