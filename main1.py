import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader
from camera import Camera
from pyrr import Vector3, vector, vector3, matrix44
from light import Light
import math
from shader import Shader

ambientColor = Vector3([0.3,0.3,0.3])
cam = Camera(Vector3([0.0, 10.0, 20.0]),Vector3([0.0, 0.0, -1.0]),Vector3([0.0, 1.0, 0.0]),Vector3([1.0, 0.0, 0.0]))

light = Light(Vector3([0.0,4.0,0.0]), Vector3([math.radians(90.0),0.0,0.0]),Vector3([2.0,2.0,2.0]))

WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
left, right, forward, backward ,up,down= False, False, False, False, False, False


# the keyboard input callback
def key_input_clb(window, key, scancode, action, mode):
    global left, right, forward, backward,up,down
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False
    if key == glfw.KEY_Q and action == glfw.PRESS:
        up = True
    elif key == glfw.KEY_Q and action == glfw.RELEASE:
        up = False
    if key == glfw.KEY_E and action == glfw.PRESS:
        down = True
    elif key == glfw.KEY_E and action == glfw.RELEASE:
        down = False



    # if key in [glfw.KEY_W, glfw.KEY_S, glfw.KEY_D, glfw.KEY_A] and action == glfw.RELEASE:
    #     left, right, forward, backward = False, False, False, False


# do the movement, call this function in the main loop
def do_movement():
    if left:
        cam.process_keyboard("LEFT", 0.05)
    if right:
        cam.process_keyboard("RIGHT", 0.05)
    if forward:
        cam.process_keyboard("FORWARD", 0.05)
    if backward:
        cam.process_keyboard("BACKWARD", 0.05)
    if up:
        cam.process_keyboard("UP", 0.05)
    if down:
        cam.process_keyboard("DOWN", 0.05)



# the mouse position callback function
def mouse_look_clb(window, xpos, ypos):
    global first_mouse, lastX, lastY

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False
    xoffset = xpos - lastX
    yoffset = lastY - ypos
    lastX = xpos
    lastY = ypos
    cam.process_mouse_movement(xoffset, yoffset)

# 设置shader文件路径
vertex_src = open("vert.vert")
fragment_src = open("frag.frag")
vertex_src1 = open("vert1.vert")
fragment_src1 = open("frag1.frag")
# the window resize callback function
def window_resize_clb(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 500)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(WIDTH, HEIGHT, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)
# ==============一些回调函数====================
# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize_clb)
# set the mouse position callback
glfw.set_cursor_pos_callback(window, mouse_look_clb)
# set the keyboard input callback
glfw.set_key_callback(window, key_input_clb)
# capture the mouse cursor
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

# make the context current
glfw.make_context_current(window)
# ================== 导入3d obj ==================
cube_indices, cube_buffer = ObjLoader.load_model("meshes/di_3.obj")
monkey_indices, monkey_buffer = ObjLoader.load_model("meshes/kelibody.obj")
floor_indices, floor_buffer = ObjLoader.load_model("meshes/floor.obj")
keliface_indices,keliface_buffer = ObjLoader.load_model("meshes/keliface.obj")
kelihair_indices,kelihair_buffer = ObjLoader.load_model("meshes/kelihair.obj")

# ================= 编译shader ==================

shader_ = Shader(vertex_src, fragment_src)
shader = shader_.ID
# ================ 设置VAO VBO =================
# VAO and VBO
VAO = glGenVertexArrays(5)
VBO = glGenBuffers(5)

# cube VAO
glBindVertexArray(VAO[0])
# cube Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, cube_buffer.nbytes, cube_buffer, GL_STATIC_DRAW)

# cube vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(0))
# cube textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(12))
# cube normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, cube_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# monkey VAO
glBindVertexArray(VAO[1])
# monkey Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, monkey_buffer.nbytes, monkey_buffer, GL_STATIC_DRAW)
# monkey vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(0))
# monkey textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(12))
# monkey normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, monkey_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# floor VAO
glBindVertexArray(VAO[2])
# floor Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, floor_buffer.nbytes, floor_buffer, GL_STATIC_DRAW)
# floor vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(0))
# floor textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(12))
# floor normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# keliface
glBindVertexArray(VAO[3])

glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
glBufferData(GL_ARRAY_BUFFER, keliface_buffer.nbytes, keliface_buffer, GL_STATIC_DRAW)
# floor vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, keliface_buffer.itemsize * 8, ctypes.c_void_p(0))
# floor textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, keliface_buffer.itemsize * 8, ctypes.c_void_p(12))
# floor normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, keliface_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# kelihair
glBindVertexArray(VAO[4])

glBindBuffer(GL_ARRAY_BUFFER, VBO[4])
glBufferData(GL_ARRAY_BUFFER, kelihair_buffer.nbytes, kelihair_buffer, GL_STATIC_DRAW)
# floor vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, kelihair_buffer.itemsize * 8, ctypes.c_void_p(0))
# floor textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, kelihair_buffer.itemsize * 8, ctypes.c_void_p(12))
# floor normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, kelihair_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)






# =================== 设置Texture =====================
textures = glGenTextures(5)
load_texture("meshes/di_3.png", textures[0])
load_texture("meshes/kelibody.png", textures[1])
load_texture("meshes/floor.jpg", textures[2])
load_texture("meshes/keliface.png", textures[3])
load_texture("meshes/kelihair.png", textures[4])

glUseProgram(shader)
# ================== 背景颜色 =========================
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)


cube_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 4, 0]))
monkey_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
keli_face_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
keli_hair_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

# ======================获取uniform再shader中的位置====================
model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")
light_pos_loc = glGetUniformLocation(shader, "lightPos")
light_color_loc = glGetUniformLocation(shader, "lightColor")
ambientColor_loc = glGetUniformLocation(shader, "ambientColor")
camera_Pos_loc = glGetUniformLocation(shader, "cameraPos")

ambient_loc = glGetUniformLocation(shader, "ambient")
diffuse_loc = glGetUniformLocation(shader, "diffuse")
specular_loc = glGetUniformLocation(shader, "specular")
shininess_loc = glGetUniformLocation(shader, "shininess")

glUniform1f(glGetUniformLocation(shader, "constant"), light.constant)
glUniform1f(glGetUniformLocation(shader, "linear"), light.linear)
glUniform1f(glGetUniformLocation(shader, "constant"), light.quadratic)


glUniform3f(ambientColor_loc, ambientColor.x,ambientColor.y,ambientColor.z)
glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    do_movement()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    trans_x = pyrr.matrix44.create_from_translation([20.0, 0, 0, 0])
    rot_y = pyrr.Matrix44.from_y_rotation(1.8 * glfw.get_time())

    # print(light.light_pos)
    # print(trans_x)
    # print(model)
    light_pos = pyrr.matrix44.create_from_translation(light.light_pos)
    light_pos = pyrr.matrix44.multiply(rot_y, light_pos)
    light_pos = pyrr.matrix44.multiply(trans_x, light_pos)

    # 在shader中灌入uniform
    glUniformMatrix4fv(glGetUniformLocation(shader, "rol"),1,GL_FALSE,light_pos)
    glUniform3f(light_pos_loc,light.light_pos.x,light.light_pos.y,light.light_pos.z)
    glUniform3f(light_color_loc, light.light_color.x,light.light_color.y,light.light_color.z)
    glUniform3f(camera_Pos_loc, cam.camera_pos.x,cam.camera_pos.y,cam.camera_pos.z)
    glUniform3f(ambient_loc, 1.0,1.0,1.0)
    glUniform3f(diffuse_loc,  1.0,1.0,1.0)
    glUniform3f(specular_loc,  0.5,0.5,0.5)
    glUniform1f(shininess_loc,32)


    # print(light_pos_loc)
    # print(light_color_loc)
    # print(ambientColor_loc)
    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)


    model = pyrr.matrix44.multiply(rot_y, cube_pos)
    model = pyrr.matrix44.multiply(trans_x, model)
    # draw the cube

    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(cube_indices))

    # draw the monkey
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, monkey_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(monkey_indices))

    # draw the floor
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

    # draw the floor
    glBindVertexArray(VAO[3])
    glBindTexture(GL_TEXTURE_2D, textures[3])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, keli_face_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(keliface_indices))
    # draw the floor
    glBindVertexArray(VAO[4])
    glBindTexture(GL_TEXTURE_2D, textures[4])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, keli_hair_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(kelihair_indices))



    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()