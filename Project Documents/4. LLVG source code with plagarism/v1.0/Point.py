import random

cur_points = {}
temp_point_n = 0


class Point:
    def __init__(self, x=None, y=None, z=None, tags=None,
                 visibility=1, highlighting=False, fillcolor='black', radius=4):
        self.highlighting = highlighting
        self.fillcolor = fillcolor
        self.radius = radius
        self.canvas_id = None
        if x is not None:
            self.x = x
        else:
            self.x = random.randint(-500, 500)
        if y is not None:
            self.y = y
        else:
            self.y = random.randint(-300, 300)
        self.z = z
        if tags is not None:
            self.tags = tags
        else:
            global temp_point_n
            self.tags = 't_p_' + str(temp_point_n)
            temp_point_n += 1

        self.visibility = visibility
        cur_points[self.tags] = self

    def draw(self, canvas):
        if self.visibility == 1:
            self.canvas_id = canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius,
                                                self.y + self.radius, fill=self.fillcolor, tags=self.tags)


# change the coordinates of the points
def changeCoords(tag, x=None, y=None):
    for tags in cur_points.keys():
        for t in tags.split():
            if t == tag:
                if x is not None:
                    cur_points[tags].x = x
                if y is not None:
                    cur_points[tags].y = y


def changeTurtleCoords(x=None, y=None):
    cur_points['turtle'].x = x
    cur_points['turtle'].x = y


def movePoint(cvs, tag, dx, dy):
    objects = cvs.find_withtag(tag)
    for obj in objects:
        # Move the point by dx and dy
        cvs.move(obj, dx, dy)
    cvs.after(50, movePoint, cvs, tag, dx, dy)  # Repeat the animation after a delay


def increment_temp_point_n(s):
    global temp_point_n
    temp_point_n += 1
    s.temp_point_n += 1
