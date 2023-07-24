cur_angles = {}


class Angle:
    def __init__(self, angle=None, ini_point=None, vertex=None, end_point=None,
                 start_angle=None, end_angle=None, tag=None, visibility=1, highlighting=False):
        self.highlighting = highlighting
        self.angle = angle
        self.ini_point = ini_point
        self.vertex = vertex
        self.end_point = end_point
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.tags = tag
        self.visibility = visibility
        self.canvas_id = None
        if self.vertex is None or self.ini_point is None or self.end_point is None:
            self.visibility = 0
        cur_angles[self.tags] = self
