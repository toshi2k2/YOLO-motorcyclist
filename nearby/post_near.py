import numpy as np
import pickle
from shapely.geometry import Point, LineString

with open('roads_pickle', 'rb') as f:    #pickle load function for reference
    roads = pickle.load(f)

with open('intersections_data', 'rb') as f:    #pickle load function for reference
    inter = pickle.load(f)

with open('near_roads', 'rb') as f:    #pickle load function for reference
    rindex = pickle.load(f)

j = []

for i,idx in enumerate(rindex):
    # print("intersection: ", i)
    # l1 = len(j)
    k = Point(inter[i])
    for midx in idx:
        for ri in list(roads[midx].coords):
            dr = k.distance(Point(ri))
            if dr < 0.001 and dr > 0.0009:
                j.append(ri)
    # l2 = len(j)
    # print("new coords for ",i ,'=', l2-l1, '\n')

print("total new coords length = ", len(j))

with open('near_inter50_100', 'wb') as f:    #pickle load function for reference
    roads = pickle.dump(j, f)

with open('near_inter50_100.txt', 'w') as fp:
    fp.write('\n'.join('%s %s' % x for x in j))