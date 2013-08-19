import sys
import random
from  graph_draw import *
random.seed(3)

depth = random.randint(10, 30)
depth = 3
max_width = 5
vertices = {}

def gen_layer(vertices, parent, layer):
    if layer>=depth:
        return None
    # print "layer:", layer
    layer += 1
    width = random.randint(1, max_width)
    #print "width:", width
    for i in range(width):
        last_id = len(vertices)
        vertices[last_id] = []
        parent.append(last_id)
        gen_layer(vertices, vertices[last_id], layer)

vertices[0] = []
gen_layer(vertices, vertices[0], 0)

visualize_graph_list(vertices, "out.png")
