import math
from shapely.geometry import Polygon

from Point import *


def randonNum(low, high):
    return random.randint(low, high)


def second_point(x, y, lg, s):
    # calculate change in x and y
    if s == float('inf'):
        delta_x = 0
        delta_y = lg
    else:
        delta_x = math.sqrt(lg ** 2 / (1 + s ** 2))
        delta_y = s * delta_x

    # calculate x2 and y2
    x2_1 = x + delta_x
    y2_1 = y + delta_y

    return x2_1, y2_1


def find_point_c(x1, y1, x2, y2, theta):
    # calculate distance AB
    ab = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # calculate vector AC with magnitude BC and angle theta
    bc = ab  # assuming BC = AB
    v = [math.cos(math.radians(theta)), math.sin(math.radians(theta))]
    ac = [bc * v[i] for i in range(2)]

    # calculate coordinates of point C
    x3 = x1 + ac[0]
    y3 = y1 + ac[1]

    return x3, y3


def calculate_orientation(p, q, r):
    # Calculate the polygon_orientation of three points (p, q, r)
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return -1


def reorder_points(points):
    points = [cur_points[i] for i in points]
    n = len(points)

    # Check if there are at least 3 points
    if n < 3:
        return []

    # Find the leftmost point (point with minimum x-coordinate)
    leftmost = min(points, key=lambda p: p.x)

    # Sort the remaining points based on their polar angle in counterclockwise order
    sorted_points = sorted(points, key=lambda p: (
        calculate_orientation(leftmost, p, Point(leftmost.x, leftmost.y + 1)),
        -((p.y - leftmost.y) / (p.x - leftmost.x) if p.x != leftmost.x else float('inf'))
    ))

    return sorted_points


def polygon_orientation(points):
    # Calculate the cross product of consecutive edges
    polygon = [[cur_points[p].x, cur_points[p].y] for p in points]
    cross_product_sum = 0
    for i in range(len(polygon)):
        current_point = polygon[i]
        next_point = polygon[(i + 1) % len(polygon)]
        cross_product_sum += (next_point[0] - current_point[0]) * (next_point[1] + current_point[1])

    # Determine the polygon_orientation based on the cross product sum
    if cross_product_sum > 0:
        return "counterclockwise"
    elif cross_product_sum < 0:
        return "clockwise"
    else:
        return "collinear"


def is_polygon(points):
    points = [cur_points[i] for i in points]
    polygon = Polygon([[p.x, p.y] for p in points])
    return polygon.is_valid


def calculate_angle(a, b, c):
    a = cur_points[a]
    b = cur_points[b]
    c = cur_points[c]
    # Calculate vectors AB and BC
    vector_ab = [a.x - b.x, a.y - b.y]
    vector_bc = [c.x - b.x, c.y - b.y]

    dot_product = vector_ab[0] * vector_bc[0] + vector_ab[1] * vector_bc[1]

    magnitude_ab = math.sqrt(vector_ab[0] ** 2 + vector_ab[1] ** 2)
    magnitude_bc = math.sqrt(vector_bc[0] ** 2 + vector_bc[1] ** 2)

    angle_rad = math.acos(dot_product / (magnitude_ab * magnitude_bc))
    angle_deg = math.degrees(angle_rad)

    return angle_deg


def edge_inclination(sp, ep):
    start_point = cur_points[sp]
    end_point = cur_points[ep]
    dx = end_point.x - start_point.x
    dy = end_point.y - start_point.y
    if dx == 0:
        if start_point.y > end_point.y:
            angle_degrees = 90
        elif start_point.y < end_point.y:
            angle_degrees = 270
        else:
            angle_degrees = 0
    elif dy == 0:
        if start_point.x < end_point.x:
            angle_degrees = 0
        elif start_point.x > end_point.x:
            angle_degrees = 180
        else:
            angle_degrees = 0
    else:
        angle = math.atan(dy / dx)  # Calculate the angle in radians
        angle_degrees = math.degrees(angle)  # Convert the angle to degrees
        if start_point.x < end_point.x:
            if start_point.y > end_point.y:
                angle_degrees *= -1
            elif start_point.y < end_point.y:
                angle_degrees = 360 - angle_degrees
        elif start_point.x > end_point.x:
            if start_point.y > end_point.y:
                angle_degrees = 180 - angle_degrees
            elif start_point.y < end_point.y:
                angle_degrees *= -1
                angle_degrees = 180 + (angle_degrees % 370)

    return angle_degrees


def point_in_direction(v, sp, ep, n):
    vertex = cur_points[v]
    start_point = cur_points[sp]
    end_point = cur_points[ep]

    direction_vector = (end_point.x - start_point.x, end_point.y - start_point.y)

    # Step 2: Normalize direction vector
    magnitude = math.sqrt((end_point.x - start_point.x) ** 2 + (end_point.y - start_point.y) ** 2)
    normalized_vector = (direction_vector[0] / magnitude, direction_vector[1] / magnitude)

    # Step 3: Calculate displacement vector
    displacement_vector = (normalized_vector[0] * n, normalized_vector[1] * n)

    # Step 4: Calculate point coordinates
    point_x = vertex.x + displacement_vector[0]
    point_y = vertex.y + displacement_vector[1]

    return point_x, point_y
