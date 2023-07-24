from Edge import *
from Angle import *

cur_polygons = {}
temp_shape_n = 0


class Poly:
    def __init__(self, count=3, edges=None, points=None, angles_tags=None, angles=None, base_length=None,
                 base_edge=None, base_angle=None, tag=None, visibility=1, highlighting=False):
        self.highlighting = highlighting
        self.edges = []
        self.angles = []
        self.points = []
        self.visibility = visibility
        self.count = count
        self.base_edge = None
        self.canvas_id = None

        if tag is not None:
            self.tags = tag
        else:
            global temp_shape_n
            self.tags = 't_sh_' + str(temp_shape_n)
            temp_shape_n += 1

        if count is not None:
            self.count = count
            if edges is not None and len(edges) == 1 and base_edge is None:
                self.base_edge = edges[0]
                if base_length is None:
                    base_length = cur_edges[self.base_edge].length
                    self.base_length = base_length
            if points is not None and len(points) >= self.count:
                self.points = points[:self.count]
                points_order(self)
                append_edges(self)
                append_angles(self)

            elif edges is not None and len(edges) >= self.count:
                self.edges = edges[:self.count]
                for i in range(self.count):
                    self.points.append(cur_edges[self.edges[i]].p1.tags)
                points_order(self)
                append_angles(self)

            elif angles_tags is not None and len(angles_tags) >= self.count:
                self.angles_tags = angles_tags[self.count]
                if self.base_edge is None:
                    if base_length is not None:
                        self.base_length = base_length
                    else:
                        self.base_length = 150
                    create_baseedge(self)
                else:
                    self.points.append(cur_edges[self.base_edge].p1)
                    self.points.append(cur_edges[self.base_edge].p2)
                find_points(self, with_tag=True)
                append_edges(self)
                append_angles(self)

            else:
                if angles is not None and len(angles) == self.count:
                    self.angles = angles
                else:
                    if base_angle is not None:
                        self.base_angle = base_angle
                    else:
                        self.base_angle = findRegularPolygonAngle(self.count)
                    self.angles = [self.base_angle] * self.count
                if self.base_edge is None:
                    if base_length is not None:
                        self.base_length = base_length
                    else:
                        self.base_length = 150
                    create_baseedge(self)
                else:
                    self.points.append(cur_edges[self.base_edge].p1.tags)
                    self.points.append(cur_edges[self.base_edge].p2.tags)
                find_points(self, with_tag=False)
                append_edges(self)
                append_angles(self)

        cur_polygons[self.tags] = self


def points_order(s):
    if not is_polygon(s.points):
        s.points = reorder_points(s.points)
        s.points = [i.tags for i in s.points]
        if polygon_orientation(s.points) == 'counterclockwise':
            s.points = s.points[::-1]


def append_edges(s):
    for i in range(s.count):
        vertex = s.points[i % s.count]
        end_point = s.points[(i + 1) % s.count]

        temp_edge = Edge(p1=vertex,
                         p2=end_point,
                         tag=vertex + end_point)
        s.edges.append(temp_edge.tags)


def append_angles(s):
    s.angles = []
    for i in range(s.count):
        ini_point = s.points[(i - 1) % s.count]
        vertex = s.points[i % s.count]
        end_point = s.points[(i + 1) % s.count]

        angle_tag = ini_point + vertex + end_point
        s.angles.append(angle_tag)

        start_angle = edge_inclination(vertex, ini_point)
        end_angle = edge_inclination(vertex, end_point)

        if start_angle < end_angle:
            extent = end_angle - start_angle
        elif start_angle > end_angle:
            extent = end_angle + 360 - start_angle
        else:
            extent = 0

        Angle(angle=extent, ini_point=ini_point, vertex=vertex, end_point=end_point, start_angle=start_angle,
              end_angle=end_angle, tag=angle_tag)


def find_points(s, with_tag):
    con_angles = []
    static_angle = 0
    for i in range(s.count):
        if with_tag:
            static_angle += (180 - cur_angles[s.angles_tags[i]].angle)
        else:
            static_angle += (180 - s.angles[i])
        con_angles.append(static_angle)
    for i in range(s.count - 2):
        t1, t2 = find_point_c(cur_points[s.points[i + 1]].x, cur_points[s.points[i + 1]].y, cur_points[s.points[i]].x,
                              cur_points[s.points[i]].y, con_angles[i])
        t_p_1 = Point(t1, t2)
        s.points.append(t_p_1.tags)


def create_baseedge(s):
    t_p_1 = Point(x=randonNum(-100, 100), y=randonNum(-100, 100))
    s.points.append(t_p_1.tags)
    t_p_2 = Point(x=(t_p_1.x + s.base_length), y=t_p_1.y)
    s.points.append(t_p_2.tags)


def findRegularPolygonAngle(n):
    if n < 3:
        print("A polygon must have at least 3 sides.")
    else:
        return (n - 2) * 180 / n
