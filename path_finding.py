import sys

# 0 - can pass
def breadth_first_search(m_map, (x_s, y_s), (x_e, y_e)):
    start = (x_s, y_s)
    end = (x_e, y_e)
    front = [start]
    checked = [start]
    tmap = [[0 for c in l ] for l in m_map]
    tmap[y_s][x_s] = 1

    neighbours = [(1, 0), (0, 1), (0, -1), (-1, 0)]

    step = 1
    h = len(m_map)
    w = len(m_map[0])
    # forward pass
    while True:
        step+=1
        print step
        #find neighbours
        new_front = []
        for x, y in front:
            for xn, yn in neighbours:
                if x+xn >= w or x+xn < 0 or y+yn >= h or y+yn < 0:
                    continue
                if m_map[y+yn][x+xn]==0 and tmap[y+yn][x+xn]==0:
                    new_front.append((x+xn, y+yn))
                    tmap[y+yn][x+xn] = step
        if new_front == []:
            return None
        front = new_front
        if end in front:
            break

    # back pass
    path = [end]
    while True:
        x, y = path[-1]
        for xn, yn in neighbours:
            if x+xn >= w or x+xn < 0 or y+yn >= h or y+yn < 0:
                continue
            v = tmap[y+yn][x+xn]
            xl, yl = path[-1]
            if v!=0 and v<tmap[yl][xl]:
                path.append((x+xn, y+yn))
                continue
        if path[-1]==start:
            break
    return path

def scale_down(m, factor):
    w = len(m[0])
    h = len(m)

    nw = w/factor
    nh = h/factor

    nm = []
    for y in range(nh):
        nm.append([])
        for x in range(nw):
            can_pass = True
            for i in range(-factor/2, factor/2):
                for j in range(-factor/2, factor/2):
                    if y*factor+i<0 or x*factor+j<0 or y*factor+i>h or x*factor+j>w:
                        continue
                    if m[y*factor+i][x*factor+j] == 1:
                        nm[-1].append(1)
                        can_pass = False
                        break
                if not can_pass:
                    break
                        
            if can_pass:
                nm[-1].append(0)
    return nm

def grow_margin(m, margin):
    w = len(m[0])
    h = len(m)

    nm = []

    for y, l in enumerate(m):
        nm.append([])
        for x, p in enumerate(l):
            can_pass = True
            for i in range(-margin/2, margin/2):
                for j in range(-margin/2, margin/2):
                    if y+i<0 or x+j<0 or y+i>=h or x+j>=w:
                        continue
                    if m[y+i][x+j] != 0:
                        nm[-1].append(1)
                        can_pass = False
                        break
                if not can_pass:
                    break
            if can_pass:
                nm[-1].append(0)

    return nm


if __name__ == "__main__":
    print "Test 1: Simple search"

    m = [[0,0,1,0,0],
         [0,0,1,0,0],
         [0,0,0,0,0],
         [0,0,1,0,0],
         [0,0,1,0,0]]
    
    print "map:"
    
    for l in m:
        print l
    
    print "path:"
    print breadth_first_search(m, (0,0), (3,0))

    print "Test 2: Big scale"
    import Image, ImageDraw
    im = Image.open("test_map_2.png")
    sz = im.size
    data = list(im.getdata())
    map2d = []
    for i, pt in enumerate(data):
        if i%sz[0] == 0:
            map2d.append([])
        if pt == (255, 255, 255):
            map2d[-1].append(0)
        else:
            map2d[-1].append(1)
#    for l in map2d:
#        print l
    #print data
    d = ImageDraw.Draw(im)
    print sz
    path = breadth_first_search(map2d, (0,0), (sz[0]-1, sz[1]-1))
    print path
    for x,y in path:
        d.point((x, y), fill="red")
    im.save("test_path_1.png")

    print "Test 3: Downscale"
    import Image, ImageDraw
    im = Image.open("test_map_2.png")
    sz = im.size
    data = list(im.getdata())
    map2d = []
    for i, pt in enumerate(data):
        if i%sz[0] == 0:
            map2d.append([])
        if pt == (255, 255, 255):
            map2d[-1].append(0)
        else:
            map2d[-1].append(1)


    factor = 2
    new_map = scale_down(map2d, 2)
    print "new_map:", new_map

    im2 = Image.new("RGB", (sz[0]/factor, sz[1]/factor), "white")
    d = ImageDraw.Draw(im2)
    for y, l in enumerate(new_map):
        for x, p in enumerate(l):
            d.point((x, y), fill=("white" if p == 0 else "black"))
    im2.save("test_downscale.png")

    print "Test 4: Grow margin"
    import Image, ImageDraw
    im = Image.open("test_map_2.png")
    sz = im.size
    data = list(im.getdata())
    map2d = []
    for i, pt in enumerate(data):
        if i%sz[0] == 0:
            map2d.append([])
        if pt == (255, 255, 255):
            map2d[-1].append(0)
        else:
            map2d[-1].append(1)


    new_map = grow_margin(map2d, 20)
    print "new_map:", new_map

    im2 = Image.new("RGB", sz, "white")
    d = ImageDraw.Draw(im2)
    for y, l in enumerate(new_map):
        for x, p in enumerate(l):
            d.point((x, y), fill=("white" if p == 0 else "black"))
    im2.save("test_grow_margin.png")
    
    print "Test 5: Grow and find path"
    import Image, ImageDraw
    im = Image.open("test_map_2.png")
    sz = im.size
    data = list(im.getdata())
    map2d = []
    for i, pt in enumerate(data):
        if i%sz[0] == 0:
            map2d.append([])
        if pt == (255, 255, 255):
            map2d[-1].append(0)
        else:
            map2d[-1].append(1)

    new_map = grow_margin(map2d, 20)
    print "new_map:", new_map

    path = breadth_first_search(new_map, (0,0), (sz[0]-1, sz[1]-1))

    d = ImageDraw.Draw(im)
    for x,y in path:
        d.point((x, y), fill="red")
    im.save("test_path_at_grown_map.png")
