import pickle
import shapely
import numpy as np
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
from scipy import spatial

with open('roads_pickle', 'rb') as f:    #pickle load function for reference
    roads = pickle.load(f)

with open('intersections_data', 'rb') as f:    #pickle load function for reference
    inter = pickle.load(f)

dist = []
a = []

for i in range(len(inter)):
    # print(i)
    k = Point(inter[i])
    for r in range(len(roads)):
        dist.append(k.distance(roads[r]))
    a.append(sorted(range(len(dist)), key=lambda k: dist[k])[0:4])
    dist.clear()

with open('near_roads', 'wb') as f:    #pickle load function for reference
    roads = pickle.dump(a, f)