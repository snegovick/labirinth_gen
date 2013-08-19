import Image, ImageDraw
import math

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
