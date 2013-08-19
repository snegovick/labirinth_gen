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

m = [[0,0,1,0,0],
     [0,0,1,0,0],
     [0,0,0,0,0],
     [0,0,1,0,0],
     [0,0,1,0,0]]

print breadth_first_search(m, (0,0), (3,0))
