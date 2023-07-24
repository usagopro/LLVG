# importing necessary modules

import re
from PIL import Image, ImageTk
import tkinter as tk
import nltk

from text_processing import *
from classLecture import *
from Shape import *
from functoins import *
from animation import *

nlp = spacy.load('en_core_web_sm')

# variables

object_btn = {}
points_btn_flag = 0
edges_btn_flag = 0
sh_btn_flag = 0
popup_opened = False
popup = None
processed_lecture = []

action = None
create = ['create', 'consider', 'assume', 'imagine', 'draw', 'show', 'locate', 'suppose', 'picture', 'let']
classes = ['point', 'edge', 'angle', 'shape', 'polygon']

size = ['length', 'size', 'width', 'centimetres', 'millimetres', 'kilometres', 'metres', 'm', 'cm', 'mm', 'km']
inclination = ['slope', 'gradient', 'incline', 'inclination', 'pitch', 'grade', 'slant', 'tilt', 'steepness', 'descent']

each = ['each', 'any', 'every', 'all']
side = ['side', 'length', 'edge', 'line', 'boundary']
angle = ['angle', 'degree']

shapes = ['polygon', 'rectangle', 'square', 'triangle', 'pentagon', 'quadrilateral', 'circle', 'shape']
ed_3_sh = ['triangle']
ed_4_sh = ['quadrilateral', 'square', 'rectangle', 'rhombus', 'parallelogram', 'trapezoid', 'trapezium', 'kite',
           'isosceles trapezoid', 'irregular quadrilateral']
ed_5_sh = ['pentagon', 'regular pentagon', 'irregular pentagon', 'convex pentagon', 'concave pentagon']
ed_6_sh = ['hexagon', 'regular hexagon', 'irregular hexagon', 'convex hexagon', 'concave hexagon',
           'regular hexagonal prism']
ed_7_sh = ['heptagon', 'regular heptagon', 'irregular heptagon', 'convex heptagon', 'concave heptagon']
ed_8_sh = ['octagon', 'regular octagon', 'irregular octagon', 'convex octagon', 'concave octagon',
           'regular octagonal prism']
ed_9_sh = ['nonagon', 'regular nonagon', 'irregular nonagon', 'convex nonagon', 'concave nonagon']
ed_10_sh = ['decagon', 'regular decagon', 'irregular decagon', 'convex decagon', 'concave decagon']

cur_sentence = 0

# interface using tkinter

window = tk.Tk()


# full screen of interface

def ExitFullScreen(event):
    window.attributes("-fullscreen", False)


# Set the window size to full screen
window.attributes("-fullscreen", True)

# Bind the Escape key to exit full screen
window.bind("<Escape>", ExitFullScreen)


# important functions


def reset():
    global processed_lecture, cur_sentence, object_btn, points_btn_flag
    global edges_btn_flag, sh_btn_flag, popup_opened, popup

    cur_points.clear()
    cur_polygons.clear()
    cur_edges.clear()
    cur_angles.clear()
    processed_lecture = []
    object_btn = {}
    points_btn_flag = 0
    edges_btn_flag = 0
    sh_btn_flag = 0
    popup_opened = False
    popup = None
    processed_lecture = []


def append_lecture():
    txt = input_field.get("1.0", "end-1c")
    sentences = nltk.sent_tokenize(txt)
    lecture.extend(sentences)
    empty_textfield()


def empty_textfield():
    input_field.delete("1.0", tk.END)


# Remove the item from the canvas

def remove_item(item_id):
    if item_id in cur_points.keys():
        canvas.delete(cur_points[item_id].canvas_id)
    elif item_id in cur_edges.keys():
        canvas.delete(cur_edges[item_id].canvas_id)
    elif item_id in cur_polygons.keys():
        for point in cur_polygons[item_id].points:
            remove_item(point)
        for edge in cur_polygons[item_id].edges:
            remove_item(edge)
    elif item_id in cur_angles.keys():
        canvas.delete(cur_angles[item_id].canvas_id)


def highlight_point(point):
    if cur_points[point].highlighting:
        cur_points[point].fillcolor = '#FAFF9A'
        cur_points[point].radius = 6
    else:
        cur_points[point].fillcolor = 'black'
        cur_points[point].radius = 4

    remove_item(point)
    cur_points[point].canvas_id = None
    showPoint(point)


def highlight_edge(item):
    if cur_edges[item].highlighting:
        cur_edges[item].fill_color = '#FFD500'
        cur_edges[item].width = 3
    else:
        cur_edges[item].fill_color = 'black'
        cur_edges[item].width = 1

    remove_item(item)
    cur_edges[item].canvas_id = None
    showEdge(item)


def highlight_shape(item):
    if cur_polygons[item].highlighting:
        for edge in cur_polygons[item].edges:
            cur_edges[edge].highlighting = True
            highlight_edge(edge)
        for point in cur_polygons[item].points:
            cur_points[point].highlighting = True
            highlight_point(point)
    else:
        for edge in cur_polygons[item].edges:
            cur_edges[edge].highlighting = False
            highlight_edge(edge)
        for point in cur_polygons[item].points:
            cur_points[point].highlighting = False
            highlight_point(point)


def highlight_item(item):
    if item in cur_points.keys():
        cur_points[item].highlighting = not cur_points[item].highlighting
        highlight_point(item)
    elif item in cur_edges.keys():
        cur_edges[item].highlighting = not cur_edges[item].highlighting
        highlight_edge(item)
    elif item in cur_polygons.keys():
        cur_polygons[item].highlighting = not cur_polygons[item].highlighting
        highlight_shape(item)


def create_obj_btn(name, ele):
    object_btn[name] = tk.Button(ele, text=name, height=1, width=35,
                                 bg='#0066CC', fg='#B8965E')
    object_btn[name].bind("<Button-1>", lambda event: open_popup(event, name))
    object_btn[name].pack()
    object_btn[name].config(font=("Arial", 12, "bold"))


def destroy_btn(name):
    if name in object_btn.keys():
        object_btn[name].destroy()


def open_popup(event, name):
    global popup, popup_opened

    if popup_opened:
        popup.destroy()
        popup_opened = False
    else:
        popup = tk.Toplevel(window)
        popup.geometry("+{}+{}".format(event.x_root - (window.winfo_x() + object_btn[name].winfo_x()) - 220,
                                       event.y_root))
        popup.overrideredirect(True)  # Removes the window decorations

        # Create the buttons in the popup
        highlight = tk.Button(popup, height=1, width=20, text="highlight",
                              command=lambda: highlight_item(name), bg='#0066CC', fg='#FAFF9A')
        highlight.pack()
        highlight.config(font=("Arial", 12, "bold"))

        delete = tk.Button(popup, height=1, width=20, text="delete",
                           command=lambda: remove_item(name), bg='#0066CC', fg='#FAFF9A')
        delete.pack()
        delete.config(font=("Arial", 12, "bold"))

        popup_opened = True


def des_all_obj_btns():
    global points_btn_flag, edges_btn_flag, sh_btn_flag
    for i in cur_points.keys():
        destroy_btn(i)
    points_btn_flag = 0
    for i in cur_edges.keys():
        destroy_btn(i)
    edges_btn_flag = 0
    for i in cur_polygons.keys():
        destroy_btn(i)
    sh_btn_flag = 0


def show_objects(mode):
    global points_btn_flag, edges_btn_flag, sh_btn_flag

    if mode == 'points':
        if points_btn_flag == 0:
            for i in cur_points.keys():
                create_obj_btn(i, point_objects_div)
            points_btn_flag = 1
        else:
            for i in cur_points.keys():
                object_btn[i].destroy()
            points_btn_flag = 0
    if mode == 'edges':
        if edges_btn_flag == 0:
            for i in cur_edges.keys():
                create_obj_btn(i, edge_objects_div)
            edges_btn_flag = 1
        else:
            for i in cur_edges.keys():
                destroy_btn(i)
            edges_btn_flag = 0
    if mode == 'shapes':
        if sh_btn_flag == 0:
            for i in cur_polygons.keys():
                create_obj_btn(i, sh_objects_div)
            sh_btn_flag = 1
        else:
            for i in cur_polygons.keys():
                destroy_btn(i)
            sh_btn_flag = 0


def animateCanvas():
    global cur_sentence
    if cur_sentence < len(lecture):
        if lecture[cur_sentence] not in processed_lecture:
            prompt(lecture[cur_sentence])
            processed_lecture.append(lecture[cur_sentence])
        cur_sentence += 1
    canvas.after(10, animateCanvas)


def showPoint(tag):
    for t in cur_points.keys():
        if t == tag:
            obj = cur_points[t]
            if obj.visibility == 1:
                obj.canvas_id = canvas.create_oval(obj.x - obj.radius, obj.y - obj.radius, obj.x + obj.radius,
                                                   obj.y + obj.radius, fill=obj.fillcolor, tags=obj.tags)


def showEdge(tag):
    for t in cur_edges.keys():
        if t == tag:
            obj = cur_edges[t]
            if obj.visibility == 1:
                if obj.tags == 'x-axis' or obj.tags == 'y-axis':
                    obj.canvas_id = canvas.create_line(obj.p1.x, obj.p1.y, obj.p2.x, obj.p2.y, fill=obj.fill_color,
                                                       width=obj.width)
                else:
                    draw_line(canvas, obj)


def showAngle(tag):
    for t in cur_angles.keys():
        if t == tag:
            obj = cur_angles[t]
            if obj.visibility == 1:
                showEdge(obj.ini_point + obj.vertex)
                showEdge(obj.vertex + obj.end_point)
                n = 20
                obj.canvas_id = canvas.create_arc(cur_points[obj.vertex].x - math.sqrt(2) * n,
                                                  cur_points[obj.vertex].y - math.sqrt(2) * n,
                                                  cur_points[obj.vertex].x + math.sqrt(2) * n,
                                                  cur_points[obj.vertex].y + math.sqrt(2) * n,
                                                  start=obj.start_angle, extent=obj.angle, style=tk.ARC)


def showPolygon(tag):
    for t in cur_polygons.keys():
        if t == tag:
            obj = cur_polygons[t]
            if obj.visibility == 1:
                for i in obj.points:
                    showPoint(i)
                for i in obj.edges:
                    showEdge(i)


def remove(tag):
    for tags in cur_points.keys():
        for t in tags.split():
            if t == tag:
                obj = cur_points[tags]
                obj.visibility = 0


def drawAllPoints():
    for point in cur_points.values():
        showPoint(point.tags)


def drawAllEdges():
    for edge in cur_edges.values():
        showEdge(edge.tags)


def drawAllAngles():
    for ang in cur_angles.values():
        showAngle(ang.tags)


def createPoint(x=None, y=None, z=None, tag=None):
    Point(x=x, y=y, z=z, tags=tag)


def create_point(txt, doc):
    tags = re.findall(r'[A-Z]*', txt)
    tags = list(filter(lambda x: x != '', tags))
    tags = sorted(tags, key=len)
    if len(tags) == 0:
        tags.append(None)
    coords = Numbers(doc)
    if len(coords) == 2:
        if re.search(r'\b[xX]\b.*\b[yY]\b', txt):
            createPoint(x=float(coords[0]), y=float(coords[1]), tag=tags[0])
        elif re.search(r'\b[yY]\b.*\b[xX]\b', txt):
            createPoint(x=float(coords[1]), y=float(coords[0]), tag=tags[0])
        else:
            createPoint(x=float(coords[0]), y=float(coords[1]), tag=tags[0])
    elif len(coords) == 1:
        only_x = r'\bx\b.*(\by\b).*(unknown|not given|not specified)'
        only_y = r'\by\b.*(\bx\b).*(unknown|not given|not specified)'
        not_x = r'\bx\b.*(unknown|not given|not specified).*\by\b'
        not_y = r'\by\b.*(unknown|not given|not specified).*\bx\b'
        for_x = r'\b[xX]\b'
        for_y = r'\b[yY]\b'
        if re.search(only_x, txt):
            createPoint(x=float(coords[0]), tag=tags[0])
        elif re.search(only_y, txt):
            createPoint(y=float(coords[0]), tag=tags[0])
        elif re.search(not_x, txt):
            createPoint(y=float(coords[0]), tag=tags[0])
        elif re.search(not_y, txt):
            createPoint(x=float(coords[0]), tag=tags[0])
        elif re.search(for_x, txt):
            createPoint(x=float(coords[0]), tag=tags[0])
        elif re.search(for_y, txt):
            createPoint(y=float(coords[0]), tag=tags[0])
    elif re.search(r'\bx[-_\s]axis\b', txt):
        createPoint(y=0, tag=tags[0])
    elif re.search(r'\by[-_\s]axis\b', txt):
        createPoint(x=0, tag=tags[0])
    elif re.search(r'\borigin\b', txt):
        createPoint(x=0, y=0, tag=tags[0])


def create_edge(txt, doc):
    p1 = None
    p2 = None
    tag = None
    fill_color = 'red'
    length = None
    slope = None
    visibility = 1
    tags = re.findall(r'[A-Z]*', txt)
    tags = list(filter(lambda x: x != '', tags))
    tags = sorted(tags, key=len)

    size_pattern = '(' + '|'.join(size) + ')'
    inclination_pattern = '(' + '|'.join(inclination) + ')'
    line_attr_num = Numbers(doc)
    i_t_s = r'\b{}\b.*\b{}\b'.format(inclination_pattern, size_pattern)  # inclination and then size
    if len(line_attr_num) == 2:
        if re.search(i_t_s, txt):
            length = float(line_attr_num[1])
            slope = float(line_attr_num[0])
        else:
            length = float(line_attr_num[0])
            slope = float(line_attr_num[1])
    elif len(line_attr_num) == 1:
        only_length = r'\b{}\b.*(\b{}\b).*(unknown|not given|not specified)'.format(size_pattern, inclination_pattern)
        only_slope = r'\b{}\b.*(\b{}\b).*(unknown|not given|not specified)'.format(inclination_pattern, size_pattern)
        not_length = r'\b{}\b.*(unknown|not given|not specified).*\b{}\b'.format(size_pattern, inclination_pattern)
        not_slope = r'\b{}\b.*(unknown|not given|not specified).*\b{}\b'.format(inclination_pattern, size_pattern)
        for_length = r'\b{}\b'.format(size_pattern)
        for_slope = r'\b{}\b'.format(inclination_pattern)
        if re.search(only_length, txt):
            length = float(line_attr_num[0])
        elif re.search(only_slope, txt):
            slope = float(line_attr_num[0])
        elif re.search(not_length, txt):
            slope = float(line_attr_num[0])
        elif re.search(not_slope, txt):
            length = float(line_attr_num[0])
        elif re.search(for_length, txt):
            length = float(line_attr_num[0])
        elif re.search(for_slope, txt):
            slope = float(line_attr_num[0])

    if len(tags) == 1:
        if len(tags[0]) == 1:
            p1 = tags[0]
        else:
            tag = tags[0]
    elif len(tags) == 2:
        if len(tags[0]) == 1 and len(tags[1]) == 1:
            p1, p2 = tags[0], tags[1]
        elif len(tags[0]) == 1 and len(tags[1]) >= 2:
            p1, tag = tags[0], tags[1]
    elif len(tags) == 3:
        p1, p2, tag = tags[0], tags[1], tags[2]
    Edge(p1=p1, p2=p2, length=length, slope=slope, tag=tag, fill_color=fill_color, visibility=visibility)


def create_polygon(txt, doc, sh_attr):
    sh_attr_num = Numbers(doc)
    tags = re.findall(r'[A-Z]*', txt)
    tags = list(filter(lambda x: x != '', tags))
    tags = sorted(tags, key=len)
    for i in tags:
        if i in cur_points.keys():
            sh_attr['points'].append(i)
        elif i in cur_edges.keys():
            sh_attr['edges'].append(i)
        else:
            sh_attr['tag'] = i

    bs_len_li = ['(' + str1 + ')?' + ' ' + str2 for str1 in each for str2 in side]
    bs_len_ptr = '(' + '|'.join(bs_len_li) + '|base[-_]?length)'  # base_length pattern
    bs_ang_li = ['(' + str1 + ')?' + str2 for str1 in each for str2 in angle]
    bs_ang_ptr = '(' + '|'.join(bs_ang_li) + ')'  # base_angle pattern

    only_bs_len = r'\b{}\b.*(\b{}\b).*(unknown|not given|not specified)'.format(bs_len_ptr, bs_ang_ptr)
    only_bs_ang = r'\b{}\b.*(\b{}\b).*(unknown|not given|not specified)'.format(bs_ang_ptr, bs_len_ptr)
    not_bs_len = r'\b{}\b.*(unknown|not given|not specified).*\b{}\b'.format(bs_len_ptr, bs_ang_ptr)
    not_bs_ang = r'\b{}\b.*(unknown|not given|not specified).*\b{}\b'.format(bs_ang_ptr, bs_len_ptr)
    for_bs_len = r'\b{}\b'.format(bs_len_ptr)
    for_bs_ang = r'\b{}\b'.format(bs_ang_ptr)

    size_pattern = '(' + '|'.join(size) + ')'
    angle_pattern = '(' + '|'.join(angle) + ')'
    line_attr_num = Numbers(doc)

    only_length = r'{}.*({}).*(unknown|not given|not specified)'.format(size_pattern, angle_pattern)
    only_angle = r'{}.*({}).*(unknown|not given|not specified)'.format(angle_pattern, size_pattern)
    not_length = r'{}.*(unknown|not given|not specified).*{}'.format(size_pattern, angle_pattern)
    not_angle = r'{}.*(unknown|not given|not specified).*{}'.format(angle_pattern, size_pattern)
    for_length = r'{}'.format(size_pattern)
    for_angle = r'{}'.format(angle_pattern)

    ang_t_len_1 = r'\b{}.*\b{}'.format(angle_pattern, size_pattern)  # angle and then length
    ang_t_len_2 = r'\b{}.*\b{}'.format(bs_ang_ptr, bs_len_ptr)  # angle and then length
    len_t_ang_1 = r'\b{}.*\b{}'.format(size_pattern, angle_pattern)  # angle and then length

    start_to_len = r'(.*?)\b{}'.format(size_pattern)
    start_to_ang = r'(.*?)\b{}'.format(angle_pattern)
    len_to_ang = r'\b{}(.*?)\b{}'.format(size_pattern, angle_pattern)
    ang_to_len = r'\b{}(.*?)\b{}'.format(angle_pattern, size_pattern)
    len_to_end = r'\b{}(.*?)$'.format(size_pattern)
    ang_to_end = r'\b{}(.*?)$'.format(angle_pattern)

    num_ptr = r'(\d+(?:\.\d+)?)(?:\s*,\s*|\s+and\s+)?'

    if len(sh_attr_num) == 1:

        if re.search(only_bs_len, txt):
            sh_attr['base_length'] = float(sh_attr_num[0])
        elif re.search(only_bs_ang, txt):
            sh_attr['base_angle'] = float(sh_attr_num[0])
        elif re.search(not_bs_len, txt):
            sh_attr['base_angle'] = float(sh_attr_num[0])
        elif re.search(not_bs_ang, txt):
            sh_attr['base_length'] = float(sh_attr_num[0])
        elif re.search(for_bs_len, txt):
            sh_attr['base_length'] = float(sh_attr_num[0])
        elif re.search(for_bs_ang, txt):
            sh_attr['base_angle'] = float(sh_attr_num[0])

        elif re.search(only_length, txt):
            sh_attr['base_length'] = float(line_attr_num[0])
        elif re.search(only_angle, txt):
            sh_attr['base_angle'] = float(line_attr_num[0])
        elif re.search(not_length, txt):
            sh_attr['base_angle'] = float(line_attr_num[0])
        elif re.search(not_angle, txt):
            sh_attr['base_length'] = float(line_attr_num[0])
        elif re.search(for_length, txt):
            sh_attr['base_length'] = float(line_attr_num[0])
        elif re.search(for_angle, txt):
            sh_attr['base_angle'] = float(line_attr_num[0])

    elif len(sh_attr_num) == 2:
        if re.search(ang_t_len_1, txt) or re.search(ang_t_len_2, txt):
            sh_attr['base_angle'] = float(sh_attr_num[0])
            sh_attr['base_length'] = float(sh_attr_num[1])
        else:
            sh_attr['base_length'] = float(sh_attr_num[0])
            sh_attr['base_angle'] = float(sh_attr_num[1])

    elif len(sh_attr_num) > 2:
        if re.search(ang_t_len_1, txt):
            sub_str = re.findall(start_to_ang, txt)
            numbers = re.findall(num_ptr, sub_str[0][0])
            if len(numbers) == 0:
                sub_str_1 = re.findall(ang_to_len, txt)
                numbers = re.findall(num_ptr, sub_str_1[0][1])
                sh_attr['angles'] = [float(i) for i in numbers]
                sub_str_2 = re.findall(len_to_end, txt)
                numbers = re.findall(num_ptr, sub_str_2[0][1])
                sh_attr['lengths'] = [float(i) for i in numbers]
            else:
                sh_attr['angles'] = [float(i) for i in numbers]
                sub_str_1 = re.findall(ang_to_len, txt)
                numbers = re.findall(num_ptr, sub_str_1[0][1])
                if len(numbers) == 0:
                    sub_str_1 = re.findall(len_to_end, txt)
                    numbers = re.findall(num_ptr, sub_str_1[0][1])
                    sh_attr['lengths'] = [float(i) for i in numbers]
                else:
                    sh_attr['lengths'] = [float(i) for i in numbers]

        elif re.search(len_t_ang_1, txt):
            sub_str = re.findall(start_to_len, txt)
            numbers = re.findall(num_ptr, sub_str[0][0])
            if len(numbers) == 0:
                sub_str_1 = re.findall(len_to_ang, txt)
                numbers = re.findall(num_ptr, sub_str_1[0][1])
                sh_attr['lengths'] = [float(i) for i in numbers]
                sub_str_2 = re.findall(ang_to_end, txt)
                numbers = re.findall(num_ptr, sub_str_2[0][1])
                sh_attr['angles'] = [float(i) for i in numbers]
            else:
                sh_attr['lengths'] = [float(i) for i in numbers]
                sub_str_1 = re.findall(len_to_ang, txt)
                numbers = re.findall(num_ptr, sub_str_1[0][1])
                if len(numbers) == 0:
                    sub_str_1 = re.findall(ang_to_end, txt)
                    numbers = re.findall(num_ptr, sub_str_1[0][1])
                    sh_attr['angles'] = [float(i) for i in numbers]
                else:
                    sh_attr['angles'] = [float(i) for i in numbers]

        elif re.search(for_length, txt):
            numbers = re.findall(num_ptr, txt)
            sh_attr['lengths'] = [float(i) for i in numbers]
        elif re.search(for_angle, txt):
            numbers = re.findall(num_ptr, txt)
            sh_attr['angles'] = [float(i) for i in numbers]

    if re.search(r'equilateral triangle', txt, re.IGNORECASE):
        sh_attr['angles'] = [60, 60, 60]
    elif re.search(r'isosceles triangle', txt, re.IGNORECASE):
        if len(sh_attr['angles']) == 0 and len(sh_attr['angles_tags']) == 0:
            sh_attr['angles'] = [90, 45, 45]

    elif re.search(r'scalene triangle', txt, re.IGNORECASE):
        if len(sh_attr['angles']) == 0:
            sh_attr['angles'] = [30, 60, 90]
        elif len(sh_attr['angles']) == 1:
            sh_attr['angles'].append(randonNum((180 - sh_attr['angles'][0]) / 2, 180 - sh_attr['angles'][0]))

    elif re.search(r'right[-\s]?(angle|angled)? triangle', txt, re.IGNORECASE):
        if 90 not in sh_attr['angles']:
            sh_attr['angles'].append(90)

    elif re.search(r'acute triangle', txt, re.IGNORECASE):
        sh_attr['angles'] = [60, 60, 60]

    elif re.search(r'obtuse triangle', txt, re.IGNORECASE):
        sh_attr['angles'] = [120, 30, 30]

    elif re.search(r'isosceles right triangle', txt, re.IGNORECASE):
        sh_attr['angles'] = [90, 45, 45]
    elif re.search(r'rectangle', txt, re.IGNORECASE):
        sh_attr['angles'] = [90, 90, 90, 90]
        Point(x=-100, y=0, tags='r1')
        Point(x=100, y=0, tags='r2')
        Point(x=100, y=100, tags='r3')
        Point(x=-100, y=100, tags='r4')
        sh_attr['points'] = ['r1', 'r2', 'r3', 'r4']

    Poly(count=sh_attr['count'],
         points=sh_attr['points'],
         edges=sh_attr['edges'],
         angles_tags=sh_attr['angles_tags'],
         angles=sh_attr['angles'],
         base_edge=sh_attr['base_edge'],
         base_length=sh_attr['base_length'],
         tag=sh_attr['tag'],
         visibility=sh_attr['visibility'])


def create_object(txt, doc):
    nouns = Nouns(doc)

    if 'point' in nouns:
        create_point(txt, doc)

    # creating a line
    elif 'line' in nouns:
        create_edge(txt, doc)

    # creating a polygon
    else:
        sh_attr = {'count': None,
                   'edges': [],
                   'lengths': [],
                   'points': [],
                   'angles_tags': [],
                   'angles': [],
                   'base_length': None,
                   'base_edge': None,
                   'base_angle': None,
                   'tag': None,
                   'visibility': 1
                   }
        for i in doc:
            j = i.text.lower()
            if j in ed_3_sh:
                sh_attr['count'] = 3
                create_polygon(txt, doc, sh_attr)
            elif j in ed_4_sh:
                sh_attr['count'] = 4
                create_polygon(txt, doc, sh_attr)
            elif j in ed_5_sh:
                sh_attr['count'] = 5
                create_polygon(txt, doc, sh_attr)
            elif j in ed_6_sh:
                sh_attr['count'] = 6
                create_polygon(txt, doc, sh_attr)
            elif j in ed_7_sh:
                sh_attr['count'] = 7
                create_polygon(txt, doc, sh_attr)
            elif j in ed_8_sh:
                sh_attr['count'] = 8
                create_polygon(txt, doc, sh_attr)
            elif j in ed_9_sh:
                sh_attr['count'] = 9
                create_polygon(txt, doc, sh_attr)
            elif j in ed_10_sh:
                sh_attr['count'] = 10
                create_polygon(txt, doc, sh_attr)


def prompt(txt):
    des_all_obj_btns()
    Point(x=0, y=-500, tags='y1')
    Point(x=0, y=500, tags='y2')
    Point(x=-500, y=0, tags='x1')
    Point(x=500, y=0, tags='x2')
    Edge(p1='x1', p2='x2', tag='x-axis', fill_color='red', width=3)
    Edge(p1='y1', p2='y2', tag='y-axis', fill_color='red', width=3)
    showEdge('x-axis')
    showEdge('y-axis')

    doc = nlp(txt)
    verbs = Verbs(doc)
    global create
    for i in verbs:
        if i in create:
            create_object(txt, doc)
            break
    if re.search(r'clear canvas', txt, re.IGNORECASE):
        print('clearing canvas')
        canvas.delete('all')
        reset()

    drawAllPoints()
    drawAllEdges()


# Get the size of the canvas
WIDTH = window.winfo_screenwidth()
HEIGHT = window.winfo_screenheight()

# create interface elements in tkinter

label = tk.Label(window, text="LIVE LECTURE VISUALIZATION", height=1, width=WIDTH)
label.config(font=("Arial", 14, "bold"), fg='#FFD700', bg='#000080')
label.place(x=0, y=0)
label.config(highlightthickness=1, highlightbackground="black")
label.pack()

text_div = tk.Frame(window, bd=1, relief="solid", width=WIDTH, height=85)
text_div.pack(anchor='nw')
text_div.config(borderwidth=1, relief="solid", bg="#191970")

input_field = tk.Text(text_div, bd=1, relief="solid", width=140, height=4)
input_field.pack(side='left', anchor='nw')
input_field.config(bg="#E2FEFE", fg="#505400", font=("Arial", 12, "bold"), insertbackground="red")

# Create a button in the division
submit_button = tk.Button(text_div, text="START", width=12, height=3, command=lambda: append_lecture())
submit_button.config(font=("Arial", 14, "bold"), bg='#0066CC', fg='#F7E7CE')
submit_button.pack(side='left', anchor='nw')

# Load the microphone icon image
mic_image = Image.open("mic.png")  # Replace "mic.png" with your own image file
mic_image = mic_image.resize((80, 80), resample=Image.Resampling.LANCZOS)
mic_icon = ImageTk.PhotoImage(mic_image)

# Create a label and an image for the microphone icon in the division
mic_label = tk.Button(text_div, image=mic_icon, width=140, height=77,
                      command=lambda: toggle_listening(input_field, mic_label))
mic_label.pack(side='left', anchor='nw')
mic_label.config(bg='#0066CC')

# canvas and side tools
# canvas and side tools

cvs_tool_div = tk.Frame(window, bd=1, relief="solid")
cvs_tool_div.pack(anchor='nw')
cvs_tool_div.config(borderwidth=1, relief="solid", bg="#0066CC")

cvs_width = WIDTH - 300
cvs_height = HEIGHT - 120

canvas = tk.Canvas(cvs_tool_div, width=cvs_width - 20, height=cvs_height - 20, bg="#C0FFFF")

# change the canvas as origin based
canvas.configure(scrollregion=(-(cvs_width / 2), -cvs_height / 2, cvs_width / 2, cvs_height / 2))
canvas.pack(side='left', padx=10, pady=10)
canvas.config(highlightthickness=1, highlightbackground="black")

tool_div = tk.Frame(cvs_tool_div, width=280, height=cvs_height - 20, bg='#000080', bd=1, relief="solid")
tool_div.pack(side='top', padx=10, pady=10)
tool_div.config(borderwidth=1, relief="solid")

# Add a label inside the tool_div frame
objects_label = tk.Label(tool_div, text="Created Objects", height=2, width=27)
objects_label.config(font=("Arial", 12, "bold"), bg='#191970', fg='#F7E7CE')
objects_label.pack(padx=10, pady=10, anchor='n')

point_objects_div = tk.Frame(tool_div, height=100, width=280)
point_objects_div.pack(padx=10, pady=10, side='top', anchor='n')

edge_objects_div = tk.Frame(tool_div, height=100, width=280)
edge_objects_div.pack(padx=10, pady=10, side='top', anchor='n')

sh_objects_div = tk.Frame(tool_div, height=100, width=280)
sh_objects_div.pack(padx=10, pady=10, side='top', anchor='n')

point_objects_btn = tk.Button(point_objects_div, text='Points', height=1, width=35,
                              command=lambda: show_objects('points'))
point_objects_btn.config(font=("Arial", 12, "bold"), borderwidth=1, relief="solid", bg='#4B0082', fg='#B76E79')
point_objects_btn.pack(padx=1, pady=1, side='top', anchor='n')

edge_objects_btn = tk.Button(edge_objects_div, text='Edges', height=1, width=35,
                             command=lambda: show_objects('edges'))
edge_objects_btn.config(font=("Arial", 12, "bold"), borderwidth=1, relief="solid", bg='#4B0082', fg='#B76E79')
edge_objects_btn.pack(padx=1, pady=1, side='top', anchor='n')

sh_objects_btn = tk.Button(sh_objects_div, text='Shapes', height=1, width=35,
                           command=lambda: show_objects('shapes'))
sh_objects_btn.config(font=("Arial", 12, "bold"), borderwidth=1, relief="solid", bg='#4B0082', fg='#B76E79')
sh_objects_btn.pack(padx=1, pady=1, side='top', anchor='n')

# calling the animate function

animateCanvas()

# looping the tkinter(interface) window

window.mainloop()
