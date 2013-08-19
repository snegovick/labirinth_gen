import sys
import random
import math

from graph_draw import *
from spanning_tree import *

ROOM_SIZE_MIN = 30
ROOM_SIZE_MAX = 50
min_distance = ROOM_SIZE_MAX*2
max_distance = ROOM_SIZE_MAX*3

rooms = {}

def point_in_rect((x,y), (xr, yr, wr, hr)):
    if (x>=xr and x<xr+wr) and (y>yr and y<yr+hr):
        return True
    return False

def rect_in_rect((x1, y1, w1, h1), (x2, y2, w2, h2)):
    p1 = (x1, y1)
    p2 = (x1, y1+h1)
    p3 = (x1+w1, y1+h1)
    p4 = (x1+w1, y1)
    r = (x2, y2, w2, h2)
    if point_in_rect(p1, r) or point_in_rect(p2, r) or point_in_rect(p3, r) or point_in_rect(p4, r):
        return True
    return False

def check_if_taken((x, y, w, h), rooms):
    for k, r in rooms.iteritems():
        if rect_in_rect((x, y, w, h), r):
            return True
    return False

def rand_angle_dist():
    a = random.randint(0, 360)
    d = random.randint(min_distance, max_distance)
    return a, d

def rand_w_h():
    w = random.randint(ROOM_SIZE_MIN, ROOM_SIZE_MAX)
    h = random.randint(ROOM_SIZE_MIN, ROOM_SIZE_MAX)
    return w, h

def find_boundaries(rooms):
    left = 0
    right = 0
    top = 0
    bottom = 0
    for k, v in rooms.iteritems():
        if v[0]<left:
            left = v[0]
        if v[0]+v[2]>right:
            right = v[0]+v[2]
        if v[1]<bottom:
            bottom = v[1]
        if v[1]+v[3]>top:
            top = v[1]+v[3]
    return (left, right, top, bottom)

def build_labyrinth(vertices):
    current_vertices = [0]
    w, h = rand_w_h()
    rooms[0] = (0, 0, w, h)
    connections = []

    while True:
        # traverse children
        next_vertices = []
        for cv in current_vertices:
            children = vertices[cv]
            for c in children:
                connections.append((cv, c))
                next_vertices.append(c)
                while True:
                    w, h = rand_w_h()
                    a, d = rand_angle_dist()
                    print "roomscv", rooms[cv]
                    x, y = rooms[cv][0], rooms[cv][1]
                    x_c = x+d*math.cos(a*math.pi/180)
                    y_c = y+d*math.sin(a*math.pi/180)
                    if not (check_if_taken((x_c, y_c, w, h), rooms)):
                        rooms[c] = (x_c, y_c, w, h)
                        break
        # print rooms
        if next_vertices == []:
            break
        current_vertices = next_vertices
    return connections
        

depth = 3
max_width = 2
vertices = {}
    

vertices[0] = []
gen_layer(vertices, vertices[0], 0, depth, max_width)

visualize_graph_list(vertices, "out.png")

connections = build_labyrinth(vertices)

boundaries = find_boundaries(rooms)
print "boundaries:", boundaries
xoffset = -boundaries[0]
yoffset = -boundaries[3]
width = boundaries[1]-boundaries[0]
height = boundaries[2]-boundaries[3]

print "connections", connections

draw_rooms(rooms, connections, xoffset, yoffset, int(width), int(height), "rooms.png")

