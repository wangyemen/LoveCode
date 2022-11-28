'''
爱心项目：
里面应用的相关知识/语法
pi, sin(), cos() 函数（都归为 ‘Math’ 方法）
def 函数
tkinter 包的相关知识
random 包的相关知识（随机函数）
'''

# 导入
from tkinter import *
from math import sin, cos, pi, log
import random

# 设置窗口的大小和爱心与窗口的距离
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 10

# basic function 基础功能
# 构造爱心形状
def heart_function(t):
    # 这里用到了sin(),cos()函数，不建议改动
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

    # 这里是爱心缩放的最大限度
    x *= IMAGE_ENLARGE
    y *= IMAGE_ENLARGE

    # 这里是缩放的位置
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
    return int(x), int(y)

# diffusion of particles 点的扩散
def scatter_inside(x, y, beta=0.15):
    ratiox = - beta * log(random.random())
    ratioy = - beta * log(random.random())
    dx = ratiox * (x - CANVAS_CENTER_X)
    dy = ratioy * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

# draw 画爱心
def shrink(x, y, ratio):
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

# draw 画爱心
def curve(p):
    return 2 * (2 * sin(4 * p)) / (2 * pi)

# 爱心类
class Heart:
    # build correlation function 构建相关函数（不建议改动）
    def __init__(self, frame = 60):
        self.frame = frame
        self.all_points = {}
        self._points = set()
        self._extra_points = set()
        self._inside = set()
        self.build(2000)

    # build particles  构建粒子并使它动起来
    def build(self, number):
        # Heart
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((int(x), int(y)))

        # scatter_inside
        for xx, yy in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(xx, yy, 0.05)
                self._extra_points.add((x, y))

        # inside
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y)
            self._inside.add((int(x), int(y)))

    # Let love act 让爱心动起来（按帧缩放，不建议改动）
    def calc_position(self, x, y, ratio):
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.4) # 0.4 可以改动建议不大于1，小于0.3
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1,1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1,1)
        return x - dx, y - dy

    # let love act  让爱心动起来（按帧缩放，不建议改动）
    def calc(self, frame):
        calc_position = self.calc_position
        ratio = 10 * curve(frame / 10 * pi)
        halo_radius = int(4 + 6 * (1 + curve(frame / 10 * pi)))           # 这行可以不要
        halo_number = int(3000 + 4000 * abs(curve(frame / 10 * pi) ** 2)) # 这行可以不要
        all_points = []

        # outline
        for x, y in self._points:
            x, y = calc_position(x, y, ratio)
            size = random.randint(1,3)
            all_points.append((x, y, size))

        # inner
        for x, y in self._extra_points:
            x, y = calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        # inside
        for x, y in self._inside:
            x, y = calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[frame] = all_points

    # render
    def render(self, canvas, frame):
        for x, y, size in self.all_points[frame % 20] :
            canvas.create_rectangle(x, y, x + 2, y + 2, width=0, fill="#FF7171")

# draw and redraw
def draw(root: Tk, canvas: Canvas, heart: Heart, frame=0):
    canvas.delete('all')
    heart.render(canvas, frame)
    root.after(30, draw, root, canvas, heart, frame + 1)

# Main function (Running function)
if __name__ == "__main__":
    # create a window
    root = Tk()
    # call
    canvas = Canvas(root, bg = "black", width = CANVAS_WIDTH, height = CANVAS_HEIGHT)
    canvas.pack()
    heart = Heart()
    for frame in range(20):
        heart.calc(frame)
    draw(root, canvas, heart)
    root.mainloop()
