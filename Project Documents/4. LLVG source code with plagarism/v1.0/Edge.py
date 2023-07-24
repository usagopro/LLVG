from functoins import *

cur_edges = {}
temp_edge_n = 0


class Edge:
    def __init__(self, p1=None, p2=None, length=None, slope=None, tag=None, fill_color='black', visibility=1,
                 width=1, highlighting=False):
        self.highlighting = highlighting
        self.width = width
        self.canvas_id = None
        if tag is not None:
            self.tags = tag
        else:
            global temp_edge_n
            self.tags = 't_ed' + str(temp_edge_n)
            temp_edge_n += 1
        if fill_color is not None:
            self.fill_color = fill_color
        else:
            self.fill_color = 'black'
        if p1 is not None:
            self.p1 = cur_points[p1]
            if p2 is not None:
                self.p2 = cur_points[p2]
                self.length = math.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)
                if self.p2.x == self.p1.x:
                    self.slope = float('inf')
                else:
                    self.slope = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
            else:
                if length is not None:
                    self.length = length
                else:
                    self.length = 200
                if slope is not None:
                    self.slope = slope
                else:
                    self.slope = 0
                temp_x, temp_y = second_point(self.p1.x, self.p1.y, self.length, self.slope)
                self.p2 = Point(x=temp_x, y=temp_y)
        else:
            if p2 is not None:
                self.p2 = cur_points[p2]
                if length is not None:
                    self.length = length
                else:
                    self.length = 200
                if slope is not None:
                    self.slope = slope
                else:
                    self.slope = 0
                self.p1 = Point(second_point(self.p2.x, self.p2.y, self.length, self.slope))
            else:
                if length is not None:
                    self.length = length
                else:
                    self.length = 200
                if slope is not None:
                    self.slope = slope
                else:
                    self.slope = 0
                self.p1 = Point(x=randonNum(-100, 100), y=randonNum(-100, 100))
                p2 = second_point(self.p1.x, self.p1.y, self.length, self.slope)
                self.p2 = Point(p2[0], p2[1])

        self.visibility = visibility
        cur_edges[self.tags] = self

    def draw(self, canvas):
        if self.visibility == 1:
            self.canvas_id = canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=self.fill_color,
                                                width=self.width, tags=self.tags)
