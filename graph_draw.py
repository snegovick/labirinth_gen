import Image, ImageDraw
import math
from path_finding import *

def calc_space_for_layers(vertices, parents, layers, layer):
    # calc sum of widths
    if layer not in layers:
        layers[layer] = 0

    for p in parents:
        for v in vertices[p]:
            layers[layer] += 1
        if vertices[p]!=[]:
            calc_space_for_layers(vertices, vertices[p], layers, layer+1)

def split_vertices(vertices, parents, layers, layer):
    if layer not in layers:
        layers[layer] = []

    for p in parents:
        for v in vertices[p]:
            layers[layer].append(v)
        if vertices[p]!=[]:
            split_vertices(vertices, vertices[p], layers, layer+1)

def find_edges(vertices, parents, layers, layer):
    if layer not in layers:
        layers[layer] = {}

    for p in parents:
        for v in vertices[p]:
            if p not in layers[layer]:
                layers[layer][p] = []
            layers[layer][p].append(v)
        if vertices[p]!=[]:
            find_edges(vertices, vertices[p], layers, layer+1)    

def visualize_graph_list(graph_dict, filename):
    vertices = graph_dict
    print "vertices:", vertices
    
    layers = {0: 1}
    calc_space_for_layers(vertices, [0], layers, 1)
    
    print "layers"
    print layers
    
    print "split vertices"
    
    vertex_layers = {0: [0]}
    split_vertices(vertices, [0], vertex_layers, 1)
    print "vertex_layers:", vertex_layers
    
    print "find edges"
    edges = {}
    find_edges(vertices, [0], edges, 1)
    
    print "edges"
    print edges

    layer_width = []
    for k, v in layers.iteritems():
        layer_width.append(v)
    print "max layer width:", max(layer_width)
    max_layer_width = max(layer_width)
    # single vertex consumes diameter + shift pixels
    offset = 100
    diameter = 50
    hshift = 10
    vshift = 100
    horizontal_step = diameter + hshift
    vertical_step = diameter + vshift
    center_x = (offset+max_layer_width*horizontal_step)/2.0

    x = 0
    y = 0
    print "creating image", (offset+max_layer_width*horizontal_step, len(vertex_layers)*vertical_step)
    im = Image.new("RGB", (offset+max_layer_width*horizontal_step, len(vertex_layers)*vertical_step), "white")
    d = ImageDraw.Draw(im)
    prev_layer = []

    for i, l in vertex_layers.iteritems():
        print l
        e = None
        if i in edges:
            e = edges[i]
        layer_width = len(l)*horizontal_step/2.0
        for j, v in enumerate(l):
            x = int(center_x - layer_width + j*horizontal_step)
            y = int((i+1)*vertical_step)
            d.arc([x, y, x+diameter, y+diameter], start=0, end=360,fill="black")
        if e!=None:
            for k, subverts in e.iteritems():
                x_s = int(center_x-prev_layer_width+prev_layer.index(k)*horizontal_step+diameter/2)
                y_s = int((i)*vertical_step+diameter)
                for v in subverts: 
                    x_e = int(center_x-layer_width+l.index(v)*horizontal_step+diameter/2)
                    y_e = int((i+1)*vertical_step)
                    d.line([x_s, y_s, x_e, y_e], width=5, fill="black")
                    # print "edge:", [x_s, y_s, x_e, y_e]
                
        prev_layer_width = layer_width
        prev_layer = l[:]
                
    im.save(filename)

def draw_rooms(rooms, connections, xoffset, yoffset, width, height, filename):
    print "w,h", width, height
    im = Image.new("RGB", (width, height), "white")    
    d = ImageDraw.Draw(im)
    for k, r in rooms.iteritems():
        print "room:", r
        x = r[0]+xoffset
        y = r[1]+yoffset
        box = (x, y, x+r[2], y+r[3])
        print "box:", box
        d.rectangle(box, outline="black")

    map2d = [[0 for i in range(width)] for j in range(height)]

    margin = 5

    forbidden_points = []
    for k, r in rooms.iteritems():
        for i in range(r[2]):
            for j in range(r[3]):
                x = int(r[0]+xoffset+j)
                y = int(r[1]+yoffset+i)
                forbidden_points.append((x, y))

    for (c_s, c_e) in connections:
        xs = int(rooms[c_s][0]+rooms[c_s][2]/2+xoffset)
        ys = int(rooms[c_s][1]+rooms[c_s][3]/2+yoffset)
        xe = int(rooms[c_e][0]+rooms[c_e][2]/2+xoffset)
        ye = int(rooms[c_e][1]+rooms[c_e][3]/2+yoffset)
        path = breadth_first_search(map2d, (xs, ys), (xe, ye))
        if path == None:
            continue
        for x,y in path:
            for i in range(-margin/2, margin/2):
                for j in range(-margin/2, margin/2):
                    if (x+i)<0 or (y+j)<0 or (x+i)>=width or (y+j)>=height:
                        continue
                    if (x+i, y+j) in forbidden_points:
                        continue
                    map2d[y+j][x+i] = 1
        
    im2 = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(im2)
    for y, l in enumerate(map2d):
        for x, p in enumerate(l):
            d.point((x, y), fill=("white" if p == 0 else "black"))
                
        #d.line((xs, ys, xe, ye), fill="black")
    
    im.save(filename)
    im2.save("paths.png")
