import sys
import random

WIDTH = 1000.0
LENGTH = 2000.0

ROOM_SIZE_MIN = 1.0
ROOM_SIZE_MAX = 5.0

ROOM_COUNT = 1000

taken = []

def calc_area(taken):
    area = 0
    for w, h, x, y in taken:
        area += w*h
    return area

if __name__ == "__main__":

    print "simple room gen"

    for r in range(ROOM_COUNT):
        w = random.random()*(ROOM_SIZE_MAX - ROOM_SIZE_MIN) + ROOM_SIZE_MIN
        h = random.random()*(ROOM_SIZE_MAX - ROOM_SIZE_MIN) + ROOM_SIZE_MIN
        
        while True:
            x = random.random()*(WIDTH)
            y = random.random()*(LENGTH)
            can_add = True
            for ow, oh, ox, oy in taken:
                if abs(x - ox) < w+ow:
                    can_add = False
                    break
                elif abs(y - oy) < h+oh:
                    can_add = False
                    break
            if can_add == True:
                taken.append((w, h, x, y))
                break
        print w, h, x, y, "area:", calc_area(taken), "room count:", len(taken)
