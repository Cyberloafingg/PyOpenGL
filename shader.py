import glfw
from OpenGL.GL import *

class Shader:
    def __init__(self,vertex_src,fragment_src):
        self.vertex_src = vertex_src
        self.fragment_src = fragment_src
        vertex = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)
        # 神他妈感天动地居然成功了
        glShaderSource(vertex, vertex_src)
        glShaderSource(fragment, fragment_src)
        glCompileShader(vertex)
        glCompileShader(fragment)
        self.ID = glCreateProgram()
        glAttachShader(self.ID, vertex)
        glAttachShader(self.ID, fragment)
        glLinkProgram(self.ID)
        if glGetShaderiv(vertex, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(vertex).decode())
        if glGetShaderiv(fragment, GL_COMPILE_STATUS) != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(fragment).decode())
        glDeleteShader(vertex)
        glDeleteShader(fragment)

    def use(self):
        glUseProgram(self.ID)
