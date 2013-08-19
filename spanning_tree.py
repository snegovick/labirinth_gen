import sys
import random
from  graph_draw import *
random.seed(3)


def gen_layer(vertices, parent, layer, depth, max_width):
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
        gen_layer(vertices, vertices[last_id], layer, depth, max_width)


if __name__ == "__main__":
    depth = 3
    max_width = 5
    vertices = {}
    
    
    vertices[0] = []
    gen_layer(vertices, vertices[0], 0, depth, max_width)
    
    visualize_graph_list(vertices, "out.png")
