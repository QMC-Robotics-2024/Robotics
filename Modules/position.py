import math
# define all planet id's
planet_0 = [i for i in range(0,7)]
planet_1 = [i for i in range(7,14)]
planet_2 = [i for i in range(14,21)]
planet_3 = [i for i in range(21,28)]

planets = [planet_0,planet_1,planet_2,planet_3]
def zone_parse(zone):
    match zone:
        case 0:
            base = planet_0
        case 1:
            base = planet_1
        case 2:
            base = planet_2
        case 3:
            base = planet_3
    return base

def organise(base): # home, left, opposite, right
    org_zones = []
    for i in range(0,4):
        index = (planets.index(base) + i) % len(planets)
        trg_base = planets[index]
        # trg_mid = sum(trg_base) // len(trg_base)
        org_zones.append(trg_base)
    return org_zones

'''
Scan for positional markers

IF most belong to our base, target middle of base and go (INDEX 0)
ELIF most belong to left base, keep turning left until ours is mid (INDEX 1)
ELIF most belong to right, turn keep turning right until ours is mid (INDEX 3)
ELSE turn 180 (INDEX 2)

'''
'''
def poses(base): # may need to explain this in person...
    opposite_base, opposite_mid = opposite(base)
    poses = []
    for markers in opposite_base: # [-3, -2, -1, 0, 1, 2, 3]
        poses.append(markers - opposite_mid)
    print(poses)
poses(bs)

'''
